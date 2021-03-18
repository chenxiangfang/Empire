from __future__ import print_function

from builtins import object
from builtins import str

from lib.common import helpers


class Module(object):

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Get-ADIDNSPermission',

            'Author': ['@Kevin-Robertson', '@snovvcrash'],

            'Description': ('Query a DACL of an ADIDNS node or zone in the specified domain. Part of Powermad.'),

            'Software': '',

            'Techniques': ['T1069'],

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : True,
            
            'Language' : 'powershell',

            'MinLanguageVersion' : '2',
            
            'Comments': [
                'https://github.com/Kevin-Robertson/Powermad'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'DistinguishedName' : {
                'Description'   :   'Distinguished name for the ADIDNS zone. Do not include the node name.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Domain' : {
                'Description'   :   'The targeted domain in DNS format. This parameter is required when using an IP address in the DomainController parameter.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'DomainController' : {
                'Description'   :   'Domain controller to target. This parameter is mandatory on a non-domain attached system.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Node' : {
                'Description'   :   'The ADIDNS node name.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Partition' : {
                'Description'   :   '(DomainDNSZones,ForestDNSZones,System) The AD partition name where the zone is stored. By default, this function will loop through all three partitions.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Zone' : {
                'Description'   :   'The ADIDNS zone to search for.',
                'Required'      :   False,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=''):
        
        moduleName = self.info['Name']
        
        # read in the common powerview.ps1 module source code
        moduleSource = self.mainMenu.installPath + '/data/module_source/situational_awareness/network/powermad.ps1'

        try:
            f = open(moduleSource, 'r')
        except:
            print(helpers.color('[!] Could not read module source path at: ' + str(moduleSource)))
            return ''

        moduleCode = f.read()
        f.close()

        # get just the code needed for the specified function
        script = helpers.strip_powershell_comments(moduleCode)

        script += '\n' + moduleName + ' '

        for option,values in self.options.items():
            if option.lower() != 'agent':
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == 'true':
                        # if we're just adding a switch
                        script += ' -' + str(option)
                    else:
                        script += ' -' + str(option) + ' ' + str(values['Value'])

        script += ' | Out-String | %{$_ + \"`n\"};"`n'+str(moduleName)+' completed!"'

        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        script = helpers.keyword_obfuscation(script)

        return script
