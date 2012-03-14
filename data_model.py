from elixir import *

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
	# timestamp=Field(Integer())
	sign=Field(Text())

class Citizen(Entity):
	using_options(tablename='Citizen')
	name = Field(Unicode(255))
	public_key=Field(Text())
	votes = OneToMany('Vote')
	
