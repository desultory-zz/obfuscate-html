import random
import string

class ObfuscateHTML(object):
    def __init__(self, text, size, phases, time):
        self.out_text = []
        self.clean_reference = []
        self.name_reference = []
        self.animation_phases = []
        self.clean_text = text
        if (size < len(text) * 2) :
            size = len(text) * 2
        if (phases < 1):
            self.phases = 1
        else:
            self.phases = int(phases)
        if time > 0:
            self.time = time
        else:
            self.time = 5
        self.size = int(size)
        
        self.generate_clean_reference()
        self.generate_map()
        self.generate_animation()
        self.generate_webpage()
        
        
    def get_nonce(self, size):
        while 1:
            nonce = ""
            for n in range(size):
                nonce += random.choice(string.ascii_letters)
            if nonce not in self.name_reference:
                break
        return nonce
        
    def make_css(self, input_css):
        output_text = '.' + input_css[0] + " {\n"
        for element in input_css[1]:
            output_text += '  ' + element[0] + ': ' + element[1] + ";\n"
        output_text += "}\n"
        return output_text
    
    def make_html(self, name, value):
        output_text = '<div class="' + name + '">' + value + '</div>' + "\n"
        return output_text
        
    def make_animation_css(self, name):
        output_text = '@keyframes ' + name + " {\n"
        for n in range(self.phases):
            phase_num = int(n * (100/(self.phases - 1)))
            output_text += '  ' + str(phase_num) + "%\t{left: " + str(self.animation_phases[self.name_reference.index(name)][n]) + 'px;}' + "\n"
        output_text += "}\n"
        return output_text
            
    def generate_clean_reference(self):
        for letter in self.clean_text:
            while 1:
                index = random.randint(0, self.size - 1)
                if index not in self.clean_reference:
                    self.clean_reference.append(index)
                    break
        #print("Clean reference postions: " + str(self.clean_reference))
                    
    def generate_map(self):
        for n in range(self.size):
            if n in self.clean_reference:
                for index in range(len(self.clean_reference)):
                    if self.clean_reference[index] == n:
                        self.out_text.append(self.clean_text[index])
                        self.name_reference.append(self.get_nonce(16))
            else:
                self.out_text.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
                self.name_reference.append(self.get_nonce(16))
            #print("Element " + str(n) + " name is " + self.name_reference[n] + " and value is " + self.out_text[n])
                
    def generate_animation(self):
        for n in range(self.size):
            phases = []
            
            total_size = self.size
            des_pos = int(total_size / 2)
            clean_size = len(self.clean_text)
            clean_des_pos = int(clean_size / 2)
            for p in range(self.phases):
                phases.append(random.randint(total_size * -12, total_size * 12))
            if n in self.clean_reference:
                pos = n + 1
                initial_offset = (pos - des_pos) * -12
                clean_pos = self.clean_reference.index(n)
                
                clear_offset = (clean_pos - clean_des_pos) * -12
                phases[-1] = int(initial_offset - clear_offset)
            else:
                r = 0
                start_clean = (n + 1 - des_pos + (len(self.clean_text) / 2) + 1) * -12
                end_clean = (n + 1 - des_pos - (len(self.clean_text) / 2) - 1) * -12
                while 1:
                    r = random.randint(total_size * -12, total_size * 12)
                    if(r < start_clean) or (r > end_clean):
                        break
                phases[-1] = r
            self.animation_phases.append(phases)
            
            #print("Element " + str(n) + " phase offsets are " + str(self.animation_phases[n]))
            
    
    def generate_webpage(self):
        header_name = self.get_nonce(16)
        header_content = [['display' , 'flex'], ['justify-content', 'center'], ['font-size', '20px'], ['font-family', 'monospace'], ['white-space', 'pre'], ['line-height', '20px']]
        
        elements = []
        elements.append([header_name, header_content])
        
        for n in range(self.size): 
            name = self.name_reference[n]
            element_content = [['position', 'relative'], ['animation', name + " " + str(self.time) + "s forwards"]]
            elements.append([name, element_content])
            
        webpage = "<!DOCTYPE html>\n<html>\n<head>\n<style>\n"
        out_html = ''
        out_css = ''
        for element in elements:
            out_css += self.make_css(element)
            
        for n in range(self.size):
            out_css += self.make_animation_css(self.name_reference[n])
            
        webpage += out_css
        webpage += "</style>\n<body>\n"
        
        out_html += '<div class="' + header_name + '">' + "\n"
        
        for n in range(self.size):
            out_html += self.make_html(self.name_reference[n], self.out_text[n])
                
        out_html += "</div>\n"
        webpage += out_html
        webpage += "</body>\n</html>"
        
        self.out_html = out_html
        self.out_css = out_css
        self.webpage = webpage
        
    def print_css(self):
        print(self.out_css)
        
    def print_html(self):
        print(self.out_html)
        
    def print_webpage(self):
        print(self.webpage)
        
    def write_webpage(self, filename):
        with open(filename, 'w') as f:
            f.write(self.webpage)
            f.close()
            
    def write_html(self, filename):
        with open(filename, 'a') as f:
            f.write(self.out_html)
            f.close
            
    def write_css(self, filename): 
        with open(filename, 'a') as f:
            f.write(self.out_css)
            f.close()
    
    def write_html_css(self, htmlfile, cssfile):
        with open(htmlfile, 'w') as f:
            f.write("<html>\n<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"" + cssfile + "\">\n</head>\n<body>\n")
            f.close()
        self.write_html(htmlfile)
        self.write_css(cssfile)

obj = ObfuscateHTML("asdfasdf", 0, 2, 2)
obj.print_html()
obj.print_css()

items = ['I spent way too much time making this', 'but now', 'i can make sites', 'that do this', 'extremely easily', 'which is pretty cool']  
time = 3
for item in items:
    obj = ObfuscateHTML(item, 1, 5, time)
    time += 1
    if items.index(item) == 0:
        obj.write_html_css('test.html', 'teststyle.css')
    else:
        obj.write_html('test.html')
        obj.write_css('teststyle.css')
#obj.write_html('index.html')