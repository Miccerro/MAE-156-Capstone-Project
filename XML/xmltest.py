#Test file to doubnle check XML parsing:
import xml.etree.ElementTree as ET
import time

#logon_response = '<Logon ErrorCode=”0” ErrorMessage=”Success”/>'
#May ne nothing, but the above line didnbt work b/c "" are special char
logon_response = '<Logon ErrorCode="0" ErrorMessage="Success"/>'


logon_root = ET.fromstring(logon_response) #Obtains root from xml message
# Read the value of the 'ErrorMessage' attribute
Logon_State = logon_root.get('ErrorMessage')

#print(Logon_State)

def statment():
    if Logon_State == "Success":
        print("Login is a success.") #Will replace this with some function to next be exectued, or some tag saying to move onto the next step. Still gotta wrtite this out
    else:
        print(Logon_State) #Will print error

#statment()



##Works with attributes and nested attributes: NOTE: I took an XML message and modified it
set_response = '''
<LastRemoteAddedSets ErrorCode="0" ErrorMessage="Success">
    LRAS_Data_Example
  <Set Key="0000000000001EAE">
    Set Data Example
    <nested_element attribute_data="attrubite_vale" />
  </Set>
</LastRemoteAddedSets>
'''
#Parse 
set_root = ET.fromstring(set_response)

#Get the value of the Error Message Attribute:
error_message = set_root.get('ErrorMessage')
print("Error Message:", error_message)

#Get the LastRemoteAddedSets element data:
LRAS_Text = set_root.text
print("LastRemoteAddedSets Data:", LRAS_Text.strip())
print("LastRemoteAddedSets Data type:", type(LRAS_Text))

#Gets the ("Set") Element and attribute 
set_element = set_root.find('.//Set') #.// syntax is on lib website
key_value = set_element.get('Key')
print("Key Attribute Vale within Set:",key_value)
#gets the Set data text:
set_Text = set_element.text
print("Set Text:", set_Text.strip())

#Gets the ("Nested") Element and attribute
nested_element = set_root.find('.//nested_element') 
n_value = nested_element.get('attribute_data')
print("Nested attribute:",n_value)


#if i wanted to find a child in the Set element:
#NEW_ELEMENT_NAME_element = set_element.find('.//NEW_ELEMENT_NAME') //So it looks within the already found set element
#attribute_value = NEW_ELEMENT_NAME_element.get('some_attribute_name')
#print(attribute_value)

##


