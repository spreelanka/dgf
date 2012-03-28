from elixir import *

class Law(Entity):
	using_options(tablename='Law')
	name = Field(Unicode(255))
	description = Field(Text())
	uuid = Field(Unicode(32))
	votes = OneToMany('Vote')
	
class Vote(Entity):
	using_options(tablename='Vote')
	citizen = ManyToOne('Citizen')
	law = ManyToOne('Law')
	yes_no = Field(Boolean())
	# timestamp=Field(Integer())
	sign=Field(Text())
	verified=Field(Boolean())
	fingerprint=Field(Unicode(100))
	law_uuid=Field(Unicode(32))

class Citizen(Entity):
	using_options(tablename='Citizen')
	name = Field(Unicode(255))
	fingerprint=Field(Unicode(100)) 
	public_key=Field(Text())
	votes = OneToMany('Vote')

#just a place to store all kinds of client config settings
class Configuration(Entity):
	using_options(tablename='Configuration')
	variable=Field(Unicode(255))
	value=Field(Unicode(255)) #who knows if this is a good data type
	
	
