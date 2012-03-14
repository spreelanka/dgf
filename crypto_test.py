import os
import gnupg
import time

gpg = gnupg.GPG(gnupghome='/Users/neilhudson/.gnupg')
message="blahblahblah"

# signed_message=gpg.sign(message)

print gpg.export_keys('FD981EEFA88E6B847ED5C6C8745610B1C33A092D')
exit()

print gpg.export_keys('john doe')
exit()


l=filter(lambda x: x['uids'][0]=="john doe <test_case@example.com>",gpg.list_keys(True))
print l[0]['fingerprint']

exit()
raw_stuff=map(lambda x: x['uids'][0] ,gpg.list_keys(True))
for i in raw_stuff:
	print i
	print "\n"
# print gpg.list_keys()
exit()

my_gpg_stuff={'keyid':gpg.list_keys()[2]['fingerprint'],'passphrase':'oreo'}

signed_msg=gpg.sign(message,**my_gpg_stuff)

# print signed_msg.verify() #gpg.verify(signed_msg,**my_gpg_stuff)
print signed_msg.data


verification=gpg.verify(signed_msg.data)
print verification.valid

# print signed_msg.blah()

# header="-----BEGIN PGP SIGNED MESSAGE-----\
# Hash: SHA1\
# \
# "
# text="blahblahblah"
# footer1="-----BEGIN PGP SIGNATURE-----\
# Version: GnuPG v1.4.9 (Darwin)\
# Comment: GPGTools - http://gpgtools.org\
# \
# "
# payload="iQEcBAEBAgAGBQJPSPCHAAoJEJqdJNqmNI/HkO0IAIFbiPxQMUfTmWJTqX11bfCH\
# grg//cL/ks3v5mbMRh4YejzgHdj+e9O7sCJUmxpn9Skq4jswCdZ9yKKdDjswDfRl\
# ja1xblpJYipO5hruiH+Cgix2rhNS+yhf9clGvr0RbHYqNvtuvoul87dS2E9wWyW3\
# NJOxcyKrRX5ml6kffP5cF82gSBLkZnqxJUYw5Ygc+mW/56SfcN/aUAHfKT+W8DnQ\
# qBsFDCBCN0tGpbIhKQAoP/nHGLSif4u7pfFBjYY8bNfkRbXK/CEQZFUfEH9dcsaT\
# G209FiG+QsmCzB4F+2BDGfIDX+Fanesr6Ca4DGX7wQGR0/K42sQXxXIcUm8jWT8=\
# =D6hK\
# "
# footer2="-----END PGP SIGNATURE-----"
# data=header+text+footer1+payload+footer2
# 

f = open("file_to_verify", "rb")
data = f.read()
print data

header="-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\n"
text="blahblahblah"
footer1="\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.9 (Darwin)\nComment: GPGTools - http://gpgtools.org\n\n"
# payload="iQEcBAEBAgAGBQJPSPL0AAoJEJqdJNqmNI/HnigH/0fPt6b0/hNmXbTioNIwOd9r\nqbh6KRCdjQeajY4wczyc0JtLrjPxYuqS1+COjoyrn/F4MjzHlPmmJMOjAWOrWq41\nShvblyVBFoIZpc+anm4mILq/TGZ8rXLPg/OZJI68mw/uz4joZdrGwxebZLoi/FU4\nvjELjfDgwfTSNBS7P7NT/VNkPtSWOGqRIsEUr2aSj/Kaq1bNiCad+tNi4wao5Vgu\ndxwgAOnsjAvDKn5GEKm6bdF/eV+aZUGJzXtpnpgcWHQBw6jNQGQghuDsRRanFrzx\n6kAk5BJlcBhNXD7nu/nspXQbmezTBzCfVpcFYGwYVBcjVU2jXjdcpWwJ0Xe+LZM=\n=4ys6"
payload="iQEcBAEBAgAGBQJPSPL0AAoJEJqdJNqmNI/HnigH/0fPt6b0/hNmXbTioNIwOd9rqbh6KRCdjQeajY4wczyc0JtLrjPxYuqS1+COjoyrn/F4MjzHlPmmJMOjAWOrWq41ShvblyVBFoIZpc+anm4mILq/TGZ8rXLPg/OZJI68mw/uz4joZdrGwxebZLoi/FU4vjELjfDgwfTSNBS7P7NT/VNkPtSWOGqRIsEUr2aSj/Kaq1bNiCad+tNi4wao5VgudxwgAOnsjAvDKn5GEKm6bdF/eV+aZUGJzXtpnpgcWHQBw6jNQGQghuDsRRanFrzx6kAk5BJlcBhNXD7nu/nspXQbmezTBzCfVpcFYGwYVBcjVU2jXjdcpWwJ0Xe+LZM==4ys6"
footer2="\n-----END PGP SIGNATURE-----\n\n\n"
# print len(data)
# matching_data=""
# for c in range(0,len(data)-1):
# 	if data[c]==manual_data[c]:
# 		matching_data+=data[c]
# 		if c==len(data)-2:
# 			print "we made it"
# 	else:
# 		break
# 	# print data[c]
# 	# print 
# 	# time.sleep(1)
# print c
# print matching_data
#print data[0]==manual_data[1]

print gpg.verify(header+text+footer1+payload+footer2).valid




# print signed_msg

# print gpg.sign(message,gpg.list_keys()[2])

# print str(signed_message)
# print message
# 
# # gpg = gnupg.GPG()
# print gpg.list_keys()
# ss=gpg.sign("blablahblah",**{'keyid':u'745610B1C33A092D','passphrase':'oreo'})
