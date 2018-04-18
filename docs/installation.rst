============
Installation
============

Installation of ``pysrim`` is easy via pip or conda. If you do not
have python installed on your machine and are new to python I would
suggest using `anaconda
<https://docs.anaconda.com/anaconda/install/>`_.

Available on PyPi

 - ``pip install pysrim``

Available on Conda

 - ``conda install -c costrouc pysrim``

You **do not** need to install SRIM if you are just doing
analysis. Otherwise for windows this is straightforward and normal
while for Linux and OSX you will need `wine` additionally installed.

Linux and OSX
-------------

For linux an OSX you will need to first have wine installed. See `this post <https://www.davidbaumgold.com/tutorials/wine-mac/>`_ on installation of wine on OSX. For linux you will typically be able to install wine via ``apt get install wine`` or ``yum install wine``. SRIM is `compatible <https://appdb.winehq.org/objectManager.php?sClass=version&iId=13202>`_ with wine.

Once you have wine installed run the `installer script <https://gitlab.com/costrouc/srim-python/raw/master/install.sh>`_ ``install.sh``.

Click extract and then done.

Windows
-------

A collegue of mine has gotten it to work easily on Windows but I
myself have no experience. Just download the executable at [srim.org](http://srim.org/). Next you will extract the SRIM files into a directory on your windows machine. Note the directory of installation as it will be needed from `trim.run()`.
