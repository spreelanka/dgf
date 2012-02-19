from elixir import *
metadata.bind = "sqlite:///dgf.sqlite"
metadata.bind.echo = True


class Law(Entity):
	using_options(tablename='Law')
	name = Field(Unicode(255))
	description = Field(Text())
	votes = OneToMany('Vote')
	
class Vote(Entity):
	using_options(tablename='Vote')
	citizen = ManyToOne('Citizen')
	law = ManyToOne('Law')
	yes_no = Field(Boolean())

class Citizen(Entity):
	using_options(tablename='Citizen')
	name = Field(Unicode(255))
	votes = OneToMany('Vote')
	
setup_all()
create_all()	
drop_all()
setup_all()
create_all()

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