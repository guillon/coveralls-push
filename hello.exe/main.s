// file hello.exe
// symbol main
// 
// hello.exe:     file format elf64-x86-64
// 
// 
// Disassembly of section .text:
// 
// 0000000000400526 <main>:
0x400526:	55                   	push   %rbp
0x400527:	48 89 e5             	mov    %rsp,%rbp
0x40052a:	48 83 ec 10          	sub    $0x10,%rsp
0x40052e:	89 7d fc             	mov    %edi,-0x4(%rbp)
0x400531:	48 89 75 f0          	mov    %rsi,-0x10(%rbp)
0x400535:	bf d4 05 40 00       	mov    $0x4005d4,%edi
0x40053a:	e8 c1 fe ff ff       	callq  400400 <puts@plt>
0x40053f:	b8 00 00 00 00       	mov    $0x0,%eax
0x400544:	c9                   	leaveq 
0x400545:	c3                   	retq   
