#!/usr/bin/env python
#
#
#

from __future__ import print_function
import sys

# Fail early if python version is not supported
def check_python_version():
    try:
        assert sys.hexversion >= 0x02070000
    except: # pragma: no cover
        sys.stderr.write('ERROR: python version >= 2.7 is required\n')
        sys.exit(1)
check_python_version()

# Setup reasonably quiet mode on ^C
import signal
def interrupt_handler(signum, frame):
    """ Handler for signals that require immediate exit. """
    sys.stderr.write("Interrupted by signal %d\n" % signum)
    sys.exit(128 + signum)
signal.signal(signal.SIGINT, interrupt_handler)

import json, hashlib, uuid, os, subprocess, logging, base64, getpass, tempfile

# Check optional packages
try:
    import yaml
except:
    sys.stderr.write("ERROR: please install required packages, for instance:\n")
    sys.stderr.write("    sudo apt-get install python-yaml\n")
    sys.exit(1)

# Inputs
try:
    infile = sys.argv[1]
except:
    sys.stderr.write("ERROR: missing coverage file argument\n")
    sys.exit(1)
    

def getkey():
    key_file = os.environ.get("COV_KEYFILE", None)
    key = os.environ.get("COV_KEY", None)
    if key_file:
        with open(key_file) as infile:
            key = infile.read().rstrip("\n")
        return key
    if key: return key
    key = getpass.getpass("Please provide the password key for coveralls-push:")
    return key

def download_tokens(tokens_enc_url):
    key = getkey()
    with tempfile.NamedTemporaryFile(delete=False) as infile:
        subprocess.check_call(['curl', '-L', '-s', '-S', '-k', tokens_enc_url], stdout=infile)
        infile.flush()
        proc = subprocess.Popen(['openssl', 'aes-256-cbc', '-d', '-a', '-pass', 'stdin', '-in', infile.name],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    (tokens, errors) = proc.communicate(input=key)
    if proc.returncode != 0:
        logging.error("Could not autheticate, invalid password key")
        sys.exit(1)
    return tokens

# Adjust level here (logging.INFO/DEBUG)
logging.basicConfig(level=logging.DEBUG)

gid = str(uuid.uuid4())[:8]

# Configuration
dryrun = os.getenv("COV_DRYRUN", None)
service_name = "coveralls-push"
coveralls_api_url = "https://coveralls.io/api/v1/jobs"
github_com = "github.com"
tokens_enc_url = "https://github.com/guillon/coveralls-push/releases/download/v0.1/coveralls-push-tokens.enc"
github_repo = 'guillon/coveralls-push'
github_url = "https://%s/%s" % (github_com, github_repo)
user_name = os.environ.get("COV_USER", os.environ.get("USER", 'coveralls-push'))
user_email = '%s@coveralls-push.github.io' % user_name
commit_message = 'Coverage data pushed by %s' % user_email

# Check tools
checks = { 'curl': [ 'curl', '-k', '-IL', 'https://%s' % github_com ],
           'git': [ 'git', 'ls-remote', 'https://%s/%s' % (github_com, github_repo)],
           'openssl': [ 'openssl', 'aes-256-cbc', '-e', '-a', '-k', '' ]
}
for tool in ['curl', 'git', 'openssl']:
    try:
        with open(os.devnull, "w+") as devnull:
            subprocess.check_call(checks[tool], stdout=devnull, stderr=devnull, stdin=devnull)
    except:
        sys.stderr.write("ERROR: %s tool not available or misconfigured network, please install. For instance:\n" % tool)
        sys.stderr.write("    sudo apt-get install curl git openssl\n")
        sys.exit(1)
        

# Get tokens
tokens = yaml.load(download_tokens(tokens_enc_url))
github_account = tokens['github_account']
github_token = tokens['github_token']
coveralls_token = tokens['coveralls_token']

# Local data set
data_basedir = "coveralls-data"

# Read yaml coverage input
with open(infile) as f:
    incov = yaml.load(f)

# Prepare data dir (also the orphean branch name that we will create on github)
try:
    os.makedirs(data_basedir)
except:
    pass
data_dir = os.path.join(data_basedir, gid)
branch_name = data_dir
logging.info("Coverage data dir: %s" % data_dir)
os.mkdir(data_dir, 0700)

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
    try:
        os.makedirs(os.path.dirname(data_filename))
    except:
        pass
    with open(data_filename, "w") as out:
        out.write(source)

github_url_with_token = 'https://%s:%s@%s/%s' % (github_account, github_token, github_com, github_repo)
gitlog_file = os.path.join(data_dir, "gitlog_file")
logging.info("Push files to github / branch: %s / %s (log in %s)" % (github_url, branch_name, gitlog_file))
with open(gitlog_file, "w") as logfile:
    subprocess.check_call(['git', '-C', files_dir, 'init'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'user.name', user_name], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'user.email', user_email], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'config', '--local', '--add', 'http.sslVerify', 'false'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'add', '.'], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'commit', '-m', commit_message], stdout=logfile, stderr=logfile)
    subprocess.check_call(['git', '-C', files_dir, 'remote', 'add', 'origin', github_url_with_token], stdout=logfile, stderr=logfile)
    if not dryrun:
        subprocess.check_call(['git', '-C', files_dir, 'push', 'origin', 'HEAD:refs/heads/%s' % branch_name], stdout=logfile, stderr=logfile)

    gitrev_file = os.path.join(data_dir, "gitrev_file")
    with open(gitrev_file, "w") as outfile:
        subprocess.check_call(['git', '-C', files_dir, 'rev-parse', 'HEAD'], stdout=outfile, stderr=logfile)
    with open(gitrev_file) as infile:
        git_revision = infile.read().rstrip("\n")
logging.info("Succesfully created git revision: %s" % (git_revision))

json_file = os.path.join(data_dir, "json_file")
logging.info("Create json post file: %s" % (json_file))

coveralls = {
    'repo_token': coveralls_token,
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
if dryrun:
    print("Completed dryrun. Nothing pushed.")
    sys.exit(0)

with open(response_file, "w") as outfile:
    subprocess.check_call(['curl', '-L', '-s', '-S', '-k', '-Fjson_file=@%s' % json_file, coveralls_api_url], stdout=outfile)
with open(response_file) as infile:
    response = json.load(infile)
message = response.get('message', None)
url = response.get('url', None)
if not message or not url:
    logging.error("Failed to push coverage data")
    sys.exit(1)

print("")
print("Succesfully pushed coverage")
print("Identifier: %s" % message)
print("Browse at: %s" % url)
