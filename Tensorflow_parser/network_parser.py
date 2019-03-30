from lark import Lark, Transformer
import json
import os
from lark.tree import pydot__tree_to_png  # Just a neat utility function
import shutil
import sys
import re

if len(sys.argv)<2:
    print('please input the network name')
    exit()
else:
    network_path=sys.argv[1]
    network_name=network_path.split('/')[-1]
    if len(sys.argv)>=3:
        python_path = sys.argv[2]
    else:
        python_path =''
# parameters
convPath = "param/conv.txt"
maxPoolPath = "param/maxpool.txt"
reluFcPath = "param/relufc.txt"
rnnPath = "param/rnn.txt"




def extractNetwork(tfFile, python_path='',debug=False):
    def update_layer_number(t):
        return  t+ '_update()\n'
    def getTab(line):
        i = 0
        while i != len(line):
            if line[i] != ' ' and line[i] != '\t':
                break
            i += 1
        tab = line[0:i]
        sentence = line[i:].strip('\n').replace(' ', '')
        return tab, sentence

    def parseConv(tree, s, tab):
        output = tree.children[0].children[0].value if tree.children[0].data != "return" else '_tmp'
        name = output + '.name'
        outputShape = output + '.shape'
        inputShape = tree.children[1].children[0] + '.shape'
        kernelShape = tree.children[2].children[0] + '.shape'
        stride = tree.children[3].children[0] + '[1:-1]'
        print_message = update_layer_number(tab)
        print_message += tab + 'print(_layer_number,"|", %s ,"|", %s ,"|", %s ,"|", %s,file = f)\n' % (outputShape, inputShape, kernelShape, stride)
        if tree.children[0].data != "return":
            return tab + s + '\n' + print_message
        else:
            return tab + '_tmp =' + s[6:] + '\n' + \
                   print_message + \
                   tab + 'return _tmp\n'

    def parseReluFc(tree, s, tab):
        output = tree.children[0].children[0].value if tree.children[0].data != "return" else '_tmp'
        name = output + '.name'
        outputShape = output + '.shape'
        inputShape = tree.children[1].children[0] + '.shape'
        kernelShape = tree.children[2].children[0] + '.shape'
        print_message = update_layer_number(tab)
        print_message += tab +'print(_layer_number,"|", %s ,"|", %s ,"|", %s ,file = f)\n' % (outputShape, inputShape, kernelShape)
        if tree.children[0].data != "return":
            return tab + s + '\n' + print_message
        else:
            return tab + '_tmp =' + s[6:] + '\n' + \
                   print_message + \
                   tab + 'return _tmp\n'

    def parserMaxpool(tree, s, tab):
        output = tree.children[0].children[0].value if tree.children[0].data != "return" else '_tmp'
        name = output + '.name'
        outputShape = output + '.shape'
        inputShape = tree.children[1].children[0] + '.shape'
        ksize = tree.children[2].children[0] + '[1:-1]'
        stride = tree.children[3].children[0] + '[1:-1]'
        print_message = update_layer_number(tab)
        print_message += tab +'print(_layer_number,"|", %s ,"|", %s ,"|", %s ,"|", %s,file = f)\n' % (outputShape, inputShape, ksize, stride)
        if tree.children[0].data != "return":
            return tab + s + '\n' + print_message
        else:
            return tab + '_tmp =' + s[6:] + '\n' + \
                   print_message + \
                   tab + 'return _tmp\n'

    def parserRnn(tree, s, tab):
        outputs = tree.children[0].value
        states = tree.children[1].value
        inputs = tree.children[3].children[0]
        name = outputs + '[0].name'
        output_timeStep = 'len(' + outputs + ')'
        n_output = outputs + '[0].shape'
        input_timeStep = 'len(' + inputs + ')'
        n_input = inputs + '[0].shape'
        n_hidden = states + '[0].shape'
        print_message = update_layer_number(tab)
        print_message += tab + 'print(_layer_number,"|",%s,"|", %s ,"|", %s ,"|", %s ,"|", %s ,file = f)\n' % (
            input_timeStep, n_input, output_timeStep, n_output, n_hidden)
        return tab + s + '\n' + print_message

    class EvalExpressions(Transformer):
        def exp(self, args):
            return args[0]

        def expy(self, args):
            return '(' + args[0] + ')'

        def expf(self, args):
            return '[' + args[0] + ']'

        def normexp(self, args):
            return args[0].value

        def sexp(self, args):
            return args[0].value

        def exps(self, args):
            return ' '.join(args)

    l = Lark('''start: conv2d | relufc  | maxpool | rnn
               
                conv2d: output [{0}] "conv2d(" input "," kernel "," strides "," padding ["," other] ")"
                rnn: VARIABLE "," VARIABLE "=" ["tf."] "rnn.static_rnn(" cell "," input ["," other] ")"
                relufc: output [{0}] "relu_layer(" input "," kernel "," biases ["," other] ")"
                maxpool: output [{0}] "max_pool(" input "," ksize "," strides "," padding ["," other] ")"
                
                output: VARIABLE "=" 
                        | "return" -> return 
                other: /[^)]+/
                input: exp
                cell: ["cell" "="] exp
                kernel: ["kernel" "="] exp
                ksize: ["ksize" "="]exp
                strides: ["strides" "="] exp
                padding: ["padding" "="] exp 
                biases: ["biases" "="] exp           
                               
                exp:  expy
                    |  expf
                    | normexp                    
                expy: "(" exps ")"
                expf:"[" exps "]"
                VARIABLE:   /[a-zA-Z_][a-zA-Z0-9_]*/
                normexp: /[^,()[\]=]+/
                exps: ( expy | sexp | expf ) +
                sexp:/[^()[\]]+/
                %ignore " "           // Disregard spaces in text

             '''.format('"tf.nn."| "tensorflow.nn." | "nn."'))

    def main():
        newFile = ''
        tree_modifier = {'conv2d': parseConv, 'relufc': parseReluFc, 'maxpool': parserMaxpool, 'rnn': parserRnn}
        path_map = {'conv2d': convPath, 'relufc': reluFcPath, 'maxpool': maxPoolPath, 'rnn': rnnPath}
        # claer files
        for path in path_map.values():
            open(path, 'w')

        with open(tfFile, 'r', encoding="utf-8") as f:
            file = f.readlines()
            for line in file:
                tab, sentence = getTab(line)
                tree = ''
                try:
                    tree = EvalExpressions().transform(l.parse(sentence))
                except Exception:
                    newFile += line
                if tree != '':
                    newFile += tab + 'f = open("%s", "a")\n' % (path_map[tree.children[0].data])
                    newFile += tree_modifier[tree.children[0].data](tree.children[0], sentence, tab)

        with open('tmpFile.py', 'w', encoding="utf-8") as f:
            if not any(['from __future__ import print_function' in i for i in file]):
                f.write('from __future__ import print_function\n')
                f.write('_layer_number = 0\n')
                f.write('def _update():\n    global _layer_number\n    _layer_number+=1\n')
                f.write(newFile)
            else:
                newFileLines = newFile.split('\n')
                critic_line = -1
                for i in range(len(newFileLines)-1,-1,-1):
                    if 'from __future__ import' in newFileLines[i]:
                        critic_line = i
                        break
                newFileLines.insert(critic_line+1,'_layer_number = 0\n'+'def _update():\n    global _layer_number\n    _layer_number+=1\n')
                f.write('\n'.join(newFileLines))
        os.system(python_path+'python tmpFile.py')
        if not debug:
            os.remove("tmpFile.py")

    def test():
        tree = EvalExpressions().transform(
            l.parse("output = tf.nn.conv2d(input_op, kernel,(1,dh,dw,1),padding='SAME')"))

        pydot__tree_to_png(tree, "conv2d.png")

    # test()
    main()


def modify_format(modelName):
    def replace_param(origin, new):
        for key in new.keys():
            if new[key]!='?':
                origin[key] = new[key].strip()
            else:
                del origin[key]
        return origin

    def transform(d):
        return str(json.dumps(d, indent=2)).replace(',', '').replace('"', '').replace(':', ' =')

    def write_file(file_name, model_name, layer_type, layer_number, input_param, output_param, weight_param,
                   hidden_param):
        default_input_param = dict().fromkeys(['input_batch', 'input_x', 'input_y', 'input_channel'], '1')
        default_output_param = dict().fromkeys(['output_batch', 'output_x', 'output_y', 'output_channel'], '1')
        default_hidden_param = dict().fromkeys(['hidden_x', 'hidden_y', 'hidden_channel'], '0')
        default_weight_param = dict().fromkeys(
            ['weight_x', 'weight_y', 'weight_channel', 'weight_number', 'stride_x', 'stride_y'], '1')
        with open(file_name, 'w') as f2:
            f2.write('Model_Name = ' + re.sub('\.py','',model_name) + '\n')
            f2.write('Layer_Type = ' + layer_type + '\n')
            f2.write('Layer_Number = ' + layer_number + '\n\n')
            ip = replace_param(default_input_param,input_param)
            #ip['input_batch']='1'
            op = replace_param(default_output_param,output_param)
            #op['output_batch']='1'
            wp = replace_param(default_weight_param,weight_param)
            if wp['stride_x']==wp['stride_y']:
                wp['weight_stride']=wp['stride_x']
                wp.pop('stride_x')
                wp.pop('stride_y')
            f2.write('Input_parameter ' + transform(ip) + '\n\n')
            f2.write('Output_parameter ' + transform(op) + '\n\n')
            f2.write('Weight_parameter ' + transform(wp) + '\n\n')
            f2.write('Hidden_parameter ' + transform(replace_param(default_hidden_param,hidden_param)))

    def modify_conv():
        with open(convPath, 'r') as f:
            for line in f.readlines():
                number, outputShape, inputShape, kernelShape, stride = line.split('|')
                outputShape = outputShape[2:-2].split(',')
                inputShape = inputShape[2:-2].split(',')
                kernelShape = kernelShape[2:-2].split(',')
                stride = stride[2:-2].split(',')
                Input_param = dict(zip(['input_batch', 'input_x', 'input_y', 'input_channel'], inputShape))
                Output_param = dict(zip(['output_batch', 'output_x', 'output_y', 'output_channel'], outputShape))
                Weight_param = dict(
                    zip(['weight_x', 'weight_y', 'weight_channel', 'weight_number', 'stride_x', 'stride_y'],
                        kernelShape + stride))
                filename = 'param/Model_parameter_' + number.strip() + '.txt'
                write_file(filename, modelName, 'CONV', number.strip(), Input_param, Output_param, Weight_param,
                           dict())

    def modify_maxpool():
        with open(maxPoolPath, 'r') as f:
            for line in f.readlines():
                number, outputShape, inputShape, kernelShape, stride = line.split('|')
                outputShape = outputShape[2:-2].split(',')
                inputShape = inputShape[2:-2].split(',')
                kernelShape = kernelShape[2:-2].split(',')
                stride = stride[2:-2].split(',')
                Input_param = dict(zip(['input_batch', 'input_x', 'input_y', 'input_channel'], inputShape))
                Output_param = dict(zip(['output_batch', 'output_x', 'output_y', 'output_channel'], outputShape))
                Weight_param = dict(zip(['weight_x', 'weight_y', 'stride_x', 'stride_y'], kernelShape + stride))
                filename = 'param/Model_parameter_' + number.strip() + '.txt'
                write_file(filename,modelName,'MAXPOOL',number.strip(),Input_param,Output_param,Weight_param,dict())


    def modify_relufc():
        with open(reluFcPath, 'r') as f:
            for line in f.readlines():
                number, outputShape, inputShape, kernelShape = line.split('|')
                outputShape = outputShape[2:-2].split(',')
                inputShape = inputShape[2:-2].split(',')
                kernelShape = kernelShape[2:-2].split(',')

                Input_param, Output_param, Weight_param = dict(), dict(), dict()
                Input_param['input_batch'], Input_param['input_x'] = inputShape
                Output_param['output_batch'], Output_param['output_x'] = outputShape
                Weight_param['weight_x'], Weight_param['weight_y'] = kernelShape
                filename = 'param/Model_parameter_' + number.strip() + '.txt'
                write_file(filename, modelName, 'FC', number.strip(), Input_param, Output_param, Weight_param,
                           dict())

    def modify_rnn():
        with open(rnnPath, 'r') as f:
            for line in f.readlines():
                number, input_Step, n_input, output_Step, n_output, n_hidden = line.split('|')
                n_input = n_input[2:-2].split(',')
                n_output = n_output[2:-2].split(',')
                n_hidden = n_hidden[2:-2].split(',')

                Input_param = {'input_batch': n_input[0], 'input_x':n_input[1]}
                Output_param = {'output_batch': n_output[0], 'output_x': n_output[1]}
                Hidden_param = {'hidden_x':n_hidden[1],'hidden_y':'1','hidden_channel':'1'}
                Weight_param = {'weight_y':str(int(n_input[1])+int(n_hidden[1])),'weight_x':n_hidden[1]}
                filename = 'param/Model_parameter_' + number.strip() + '.txt'
                write_file(filename, modelName, 'RNN', number.strip(), Input_param, Output_param, Weight_param,
                           Hidden_param)

    modify_conv()
    modify_maxpool()
    modify_relufc()
    modify_rnn()

if os.path.exists('param'):
    shutil.rmtree('param')
os.mkdir('param')
extractNetwork(network_path,python_path,True)
modify_format(network_name)
