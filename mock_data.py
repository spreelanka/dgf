from elixir import *
from data_model import *
metadata.bind = "sqlite:///dgf.sqlite"
metadata.bind.echo = True
	
setup_all()
create_all()	
drop_all()
setup_all()
create_all()


c=Configuration()
c.variable='gnupghome'
c.value='/Users/neilhudson/.gnupg'

# c2=Configuration()
# c2.variable='junkvar'
# c2.value='1'

c3=Configuration()
c3.variable='default_user'
c3.value='john doe <test_case@example.com>'

c4=Configuration()
c4.variable='gpg_keystore_path'
c4.value='~/.gnupg' 

new_law=Law()
new_law.name="golden rule"
new_law.description="goooold baby, getit getit"
new_law2=Law()
new_law2.name="test"
new_law2.description="trying this out"
new_law3=Law()
new_law3.name="other rule"
new_law3.description="don't be the other"


c=Citizen()
c.name="john doe"
c.public_key="-----BEGIN PGP PUBLIC KEY BLOCK-----\n\
Version: GnuPG v1.4.9 (Darwin)\n\
Comment: GPGTools - http://gpgtools.org\n\
\n\
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\n\
=iIxK\n\
-----END PGP PUBLIC KEY BLOCK-----\n\
"

session.commit()

# v=Vote()
# v.citizen=c
# v.law=new_law
# v.yes_no=True
# 
# v=Vote()
# v.citizen=c
# v.law=new_law2
# v.yes_no=False
# 
# v=Vote()
# v.citizen=c
# v.law=new_law3
# v.yes_no=False
session.commit()



if __name__ == "__main__":
	c=Configuration.query.filter_by(variable='junkvar').one()
	print c.variable
	print c.value
	c=Configuration.query.filter_by(variable='this_doesnt_exist').all()
	if len(c):
		print "exists!"
	else:
		print "doesn't exist!"