class CustomerProfile:

    '''
    profileName = Name of profile
    willingness_to_pay = lambda function with willingness to pay for kW
    willingness_to_wait = lambda function with willingness to wait in minutes
    

     '''
    def __init__(self, profileName, willingness_to_pay, willingness_to_wait, willingness_to_release):
        self.profileName = profileName
        self.willingness_to_pay = willingness_to_pay
        self.willingness_to_wait = willingness_to_wait
        self.willingness_to_release = willingness_to_release