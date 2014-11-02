Mojibake
========

`mojibake` is a script to "[mojibake]"-ify binary data so that it can be copy/pasted between (unicode-aware) terminals  

[mojibake]: http://en.wikipedia.org/wiki/Mojibake

Introduction
============

The [base64] format was designed to encode binary data within a set of characters that were safe for (text-only) e-mail. It was designed to be reasonably efficient -- each 8-bit base64 character can represent 6 bits of binary data. Or, 4 base64 characters represent 3 bytes of binary data.

Instead of optimizing for an efficient size transformations, what if you optimize for how many bytes you can represent in each character? Unicode has over 2^16 assigned characters, so you could represent two bytes per character!

It's not very space efficient, though. Those two bytes of binary data need 4-5 UTF-8 bytes to encode them as a unicode character. 

But it looks cool!

[base64]: http://en.wikipedia.org/wiki/Base64

Sample Use
==========

Like Bas64
----------

~~~
$ date | base64
U3VuIE5vdiAgMiAxNjozNToxNCBHTVQgMjAxNAo=

$ date | mojibake 
𥍵𦸠𤹯𧘠𢀲𢀱𣘺𣌵𣨱𣜠𤝍𥐠𣈰𣄴덦
~~~

Look at all the characters you saved!  :p

~~~
$ echo 𥍵𦸠𤹯𧘠𢀲𢀱𣘺𣌵𣨱𣜠𤝍𥐠𣈰𣄴덦 | ./mojibake --decode
Sun Nov  2 16:35:17 GMT 2014
~~~

Like `tar | base64`
-------------------

When I'm ssh-hopping around on machines, sometimes I just want to copy-paste a couple small script files somewhere. Sometimes I use `tar cz foo bar | base64` to grab them.  But it's even easier with mojibake:

~~~
$ mojibake foo bar 
𥁋𠌄𡐀𠠀𠠀隭𦉅𠀀𠀀𠀀𠀀𠸀𠀀𠌀𡰀𦙯𦽕𥐉𠀃𤉞𥙔𨁞𥙔𧕸𠬀𠄄鰪𠀀𠐔𠀀𠃳𤣍烲繺𢣏𢿊𤥑謫𠁐𤬇
𠠘乾𧬐𠀀𠀎𠀀𠁐𤬃𠐔𠀈𠀈𠀉𨕢𤔀𠀀𠀀𠀀𠁓𠀀𠀃𠀜𠁢𦅲𥕔𠤀𠍲𥹖𥒀𥹖𥑵𧠋𠀁𠓵𠄀𠀄𡐀𠀀𢗊堶𨀰
𠰄柇𢥾𠉗𢱁𤏅𠈆𡳙𥈒𪌸𢣫𡎉鶝𨜊嘏𠌩𩬄𨙊𤖟万𤈊𥝘枧𥪻𤹾𤏠𨦈堤𢎄𠵜𧃲𠷮𧍙砛𠅐𤬇𠢣𥤀靴𠀀
𠁓𠀀𠁐𤬁𠈞𠌔𠀈𠀈𠃯𨑢𤔘乾𧬐𠀀𠀎𠀀𠀃𠀘𠀀𠀀𠀁𠀀𠂤𨄀𠀀𠁦𦽯𥕔𠔀𠍂𥹖𥑵𧠋𠀁𠓵𠄀𠀄𡐀𠀀𥁋
𠄂𡸃𡐀𠠀𠠀𠦅𦉅𪍙𠃰𤬀𠀀𥌀𠀀𠌀𡠀𠀀𠀀𠄀𠀀𪒁𥴀𠀀𦉡𧉕𥐅𠀃𧉞𥙔𧕸𠬀𠄄鰪𠀀𠐔𠀀𠁐𤬅𠘀𠀀𠀂
𠀂𠂒𠀀𠃵𠀀𠀀덜
~~~

Then, on my destination machine: 

~~~
$ mojibake --unzip 
Paste the mojibaked zip file. Type '.' to finish.
𥁋𠌄𡐀𠠀𠠀隭𦉅𠀀𠀀𠀀𠀀𠸀𠀀𠌀𡰀𦙯𦽕𥐉𠀃𤉞𥙔𨁞𥙔𧕸𠬀𠄄鰪𠀀𠐔𠀀𠃳𤣍烲繺𢣏𢿊𤥑謫𠁐𤬇
𠠘乾𧬐𠀀𠀎𠀀𠁐𤬃𠐔𠀈𠀈𠀉𨕢𤔀𠀀𠀀𠀀𠁓𠀀𠀃𠀜𠁢𦅲𥕔𠤀𠍲𥹖𥒀𥹖𥑵𧠋𠀁𠓵𠄀𠀄𡐀𠀀𢗊堶𨀰
𠰄柇𢥾𠉗𢱁𤏅𠈆𡳙𥈒𪌸𢣫𡎉鶝𨜊嘏𠌩𩬄𨙊𤖟万𤈊𥝘枧𥪻𤹾𤏠𨦈堤𢎄𠵜𧃲𠷮𧍙砛𠅐𤬇𠢣𥤀靴𠀀
𠁓𠀀𠁐𤬁𠈞𠌔𠀈𠀈𠃯𨑢𤔘乾𧬐𠀀𠀎𠀀𠀃𠀘𠀀𠀀𠀁𠀀𠂤𨄀𠀀𠁦𦽯𥕔𠔀𠍂𥹖𥑵𧠋𠀁𠓵𠄀𠀄𡐀𠀀𥁋
𠄂𡸃𡐀𠠀𠠀𠦅𦉅𪍙𠃰𤬀𠀀𥌀𠀀𠌀𡠀𠀀𠀀𠄀𠀀𪒁𥴀𠀀𦉡𧉕𥐅𠀃𧉞𥙔𧕸𠬀𠄄鰪𠀀𠐔𠀀𠁐𤬅𠘀𠀀𠀂
𠀂𠂒𠀀𠃵𠀀𠀀덜
.Archive:  /var/folders/h6/y72jsht13xx_0sgnrnb3m68c0000gn/T/tmp7yidcl5k.zip
  inflating: foo                     
  inflating: bar                     
~~~

Tips
====

Fonts
-----

If you want to see the cool chinese characters instead of a screen full of boxes, 
you'll need to install [fonts] that support the unicode [CJK Unified Ideographs Extension B][CJKeB]. You may already have a font that can handle these characters. If not, I recommend the freely available [Hanazono]. 

[Hanazono]: http://fonts.jp/hanazono/
[fonts]: http://en.wikipedia.org/wiki/List_of_CJK_fonts
[CJKeB]: http://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_B




