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

class Citizen(Entity):
	using_options(tablename='Citizen')
	name = Field(Unicode(255))
	votes = OneToMany('Vote')
	
