#!/usr/bin/env python
from __future__ import print_function
import sys
try:
    import yaml, json, hashlib
    import uuid, os, subprocess
    import logging, base64
except:
    sys.stderr.write("ERROR: python2.7 and required packages must be installed\n")
    sys.stderr.write("ERROR: please install python2.7 and python-yaml package\n")
    sys.exit(1)

# Adjust level here (logging.INFO/DEBUG)
logging.basicConfig(level=logging.DEBUG)

# Inputs
infile = sys.argv[1]
gid = str(uuid.uuid4())[:8]

# Configuration
service_name = "coveralls-push"
coveralls_api_url = "https://coveralls.io/api/v1/jobs"
github_com = "github.com"
github_user = os.environ.get("COV_USER", os.environ.get("USER", 'coveralls-push'))
github_repo = 'guillon/coveralls-push'
github_url = "https://%s/%s" % (github_com, github_repo)
github_user_url = "https://%s@%s/%s" % (github_user, github_com, github_repo)
user_name = os.environ.get("USER", gid)
user_email = '%s@guillon.github.io' % user_name
commit_message = 'Coverage data pushed by %s' % user_email
coveralls_token = 'eTRIVkN5TjNHWGFMTUZTUWVTc3Z5WTR5Nlk1S2kwR0Y2'

# Local data set
data_basedir = "coveralls-data"

# Read yaml coverage input
with open(infile) as f:
    incov = yaml.load(f)

# Prepare data dir (also the orphean branch name that we will create on github)
data_dir = os.path.join(data_basedir, gid)
branch_name = data_dir
logging.info("Coverage data dir: %s" % data_dir)
os.makedirs(data_dir)

files_dir = os.path.join(data_dir, 'files')
os.makedirs(files_dir)
extension = ""
source_files = []
for symbol in incov:
    logging.info("Process symbol %s" % (symbol))
    filename =  "%s%s" % (symbol, extension)
    pairs = incov[symbol]
    source = ""
    coverage = []
    for count, line in pairs:
        source += "%s\n" % line
        coverage.append(count)
    source_digest = hashlib.md5(source).hexdigest()
    source_files.append({
        'name': filename,
        'source_digest': source_digest,
        'coverage': coverage,
        'source': source
    })
    data_filename = os.path.join(files_dir, filename)
    logging.debug("Create data filename: %s" % (data_filename))
    os.makedirs(os.path.dirname(data_filename))
    with open(data_filename, "w") as out:
        out.write(source)

gitlog_file = os.path.join(data_dir, "gitlog_file")
logging.info("Push files to github / branch: %s / %s (log in %s)" % (github_user_url, branch_name, gitlog_file))
with open(gitlog_file, "w") as logfile:
    subprocess.check_call(['git', '-C', files_dir, 'init'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'user.name', user_name], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'user.email', user_email], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'http.sslVerify', 'false'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'credential.helper', 'cache'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'remote', 'add', 'origin', github_user_url], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'add', '.'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'commit', '-m', commit_message], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'push', 'origin', 'HEAD:refs/heads/%s' % branch_name], stdout=logfile, stderr=logfile)

    gitrev_file = os.path.join(data_dir, "gitrev_file")
    with open(gitrev_file, "w") as outfile:
        subprocess.check_call(['git', '-C', files_dir, 'rev-parse', 'origin/%s' % branch_name], stdout=outfile, stderr=logfile)
    with open(gitrev_file) as infile:
        git_revision = infile.read().rstrip("\n")
logging.info("Succesfully created git revision: %s" % (git_revision))

json_file = os.path.join(data_dir, "json_file")
logging.info("Create json post file: %s" % (json_file))

coveralls = {
    'repo_token': base64.b64decode(coveralls_token),
    'service_name': service_name,
    'git': {
        'head': {
            'committer_email': user_email, 'committer_name': user_name, 'author_email': user_email, 'author_name': user_name,
            'message': commit_message, 'id': git_revision
        },
        'remotes': [
            { 'url': github_url, 'name': 'origin'}
        ],
        'branch': branch_name
    },
    'source_files': source_files
}

with open(json_file, "w") as out:
    json.dump(coveralls, out)

response_file = os.path.join(data_dir, "response_file")
logging.info("Push coverage to coveralls: %s" % (coveralls_api_url))
with open(response_file, "w") as outfile:
    subprocess.check_call(['curl', '-L', '-s', '-S', '-k', '-Fjson_file=@%s' % json_file, coveralls_api_url], stdout=outfile)
with open(response_file) as infile:
    response = json.load(infile)

message = response.get('message', None)
url = response.get('url', None)
if message and url:
    print("")
    print("Succesfully pushed coverage")
    print("Identifier: %s" % message)
    print("Browse at: %s" % url)
else:
    loggign.error("Failed to push coverage data")
    sys.exit(1)
