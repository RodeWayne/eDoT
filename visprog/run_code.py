from PIL import Image
from visprog.engine.utils import ProgramInterpreter
import gc


def preprocess(prog):
    prog = prog.strip('\n')
    eid = prog.find('\n\n')
    if eid != -1:
        prog = prog[:eid]   
    return prog


def get_result_supervised(samples, vqafunc, tokenizer):
    
    interpreter = ProgramInterpreter(dataset='gqa', vqa=vqafunc, m_tokenizer=tokenizer, loc_processor=None, loc_model=None) 
    scores = []
    for i in range(len(samples['text_input'])):
        try:
            visprog_result_score = visprog(
                interpreter=interpreter,
                image = samples['imageId'][i],
                prog = samples['program'][i],
            )
        except Exception as e:
            with open('visprog/prompts/gqa_fixed_code.prompt','r') as fixedfile:
                content = fixedfile.read()
                content = content.replace('qux', samples['text_input'][i])
                visprog_result_score = visprog(
                    interpreter=interpreter,
                    image = samples['imageId'][i],
                    prog = content,
                )
        scores.append(visprog_result_score[0])
        
    del interpreter
    gc.collect()
    return scores


def visprog(interpreter, image, prog):
    
    root = '/path/to/gqa/images/'
    if '.jpg' not in image:
        img = image + '.jpg'
    else:
        img = image
    
    
    image = Image.open(img)

    init_state = dict(
        IMAGE=[(0, image,1)]
    )

    prog = preprocess(prog)   
    if prog == None:
        prog = "connection_error"
        result = "connection_error"
        return 0
    else:
        probs, prog_state = interpreter.execute(prog, init_state, inspect=False)
        return probs
