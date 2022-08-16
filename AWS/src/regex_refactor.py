import re


def regex_file(fileName):
    new_content=''

    for line in open('%s' % fileName ,"r+"):

        if 'CREATE' in line:
            new_content = new_content + line + "\n"

        elif ';' in line:
            new_content = new_content + line + "\n"
        else:
            match = re.findall(r'(?<=\[).+?(?=\])',line)
            try:
                string = 'JSON_VAR:%s as %s,' % (match[0], match[0])
                new_content = new_content + string + "\n" 

            except IndexError: 
                pass 

    file = open('output.sql', 'w+')
    file.write(new_content)
    file.close()
    
    return print('Done')




