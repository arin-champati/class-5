from DataSources.ActiveDirectory.req_lib import ReqLib

'''
This endpoint returns information about
a user within the Princeton community.
The only parameter that the endpoint requires
is the user's netid. The parameter's name is:
uid
The return value has the following information
about the user:
displayname (Full name of the user)
universityid (PUID number)
mail (user's email address)
pustatus (is the user a graduate, undergraduate, or faculty?)
department (which department the user belongs to)
eduPersonPrimaryAffiliation (whether the user is a student or faculty)
streetAddress (office number and location if it is a faculty member)
telephoneNumber (phone number if it is a faculty member)
'''
class UserInfo:
    @staticmethod
    def getInfo(userid):
        if not userid:
            userid = ''

        req_lib = ReqLib()

        req = req_lib.getJSON(
            req_lib.configs.USERS_FULL,
            uid=userid
        )
        
        if req == [] or not req or req == 0:
            return {
            'name': '',
            'class_year': '',
            'major': '',
            'email': ''
        }
        else:
            result = {
                'name': req[0].get('displayname', ''),
                'class_year': '',
                'major': '',
                'email': req[0].get('mail', '')
            }
        return result
    
if __name__ == "__main__":
    # FOR TESTING
    user = UserInfo.getInfo("al38")

    print(user)
