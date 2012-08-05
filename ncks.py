#Optwon
#Nebcorp Kriscorp Scripts
#Helper libraryimport random

def chance(value): #Returns % value to activate. the value is 'Chance to activate', not 'Chance to fail'
	if random.random() < value:
		return True
	else:
		return False
        
def clamp(min_v,value,max_v):
    return min(max_v, max(min_v, value))