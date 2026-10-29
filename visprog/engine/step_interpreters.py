import torch
import re
import numpy as np
import io, tokenize
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from .nms import nms
from visprog.vis_utils import html_embed_image, html_colored_span, vis_masks


def parse_step(step_str,partial=False):
    tokens = list(tokenize.generate_tokens(io.StringIO(step_str).readline))
    output_var = tokens[0].string
    step_name = tokens[2].string
    parsed_result = dict(
        output_var=output_var,
        step_name=step_name)
    if partial:
        return parsed_result

    arg_tokens = [token for token in tokens[4:-3] if token.string not in [',','=']]
    num_tokens = len(arg_tokens) // 2
    args = dict()
    for i in range(num_tokens):
        args[arg_tokens[2*i].string] = arg_tokens[2*i+1].string
    parsed_result['args'] = args
    return parsed_result


def html_step_name(content):
    step_name = html_colored_span(content, 'red')
    return f'<b>{step_name}</b>'


def html_output(content):
    output = html_colored_span(content, 'green')
    return f'<b>{output}</b>'


def html_var_name(content):
    var_name = html_colored_span(content, 'blue')
    return f'<b>{var_name}</b>'


def html_arg_name(content):
    arg_name = html_colored_span(content, 'darkorange')
    return f'<b>{arg_name}</b>'


class EvalInterpreter():
    step_name = 'EVAL'

    def __init__(self):
        print(f'Registering {self.step_name} step')

    def parse(self,prog_step):
        parse_result = parse_step(prog_step.prog_str)
        step_name = parse_result['step_name']
        output_var = parse_result['output_var']
        step_input = eval(parse_result['args']['expr'])
        assert(step_name==self.step_name)
        return step_input, output_var
    
    def html(self,eval_expression,step_input,step_output,output_var):
        eval_expression = eval_expression.replace('{','').replace('}','')
        step_name = html_step_name(self.step_name)
        var_name = html_var_name(output_var)
        output = html_output(step_output)
        expr = html_arg_name('expression')
        return f"""<div>{var_name}={step_name}({expr}="{eval_expression}")={step_name}({expr}="{step_input}")={output}</div>"""

    def execute(self,prog_step,inspect=False):
        step_input, output_var = self.parse(prog_step)
        
        predictions_after_eval = {}
        
        eval_expression = step_input

        eval_vars = self.get_eval_var(eval_expression)
        if 'xor' in step_input:
            step_input = step_input.replace('xor','!=')

        if len(eval_vars) == 1:
            var_name = eval_vars[0].strip('{}')
            idx_answer_score_corpus = prog_step.state[var_name]
            
            var_name_distribution = prog_step.state[var_name+'_distribution'] 
            prog_step.state[output_var+'_distribution'] = [var_name_distribution]
            my_prog_state = {}
            for i in range(len(idx_answer_score_corpus)):
                idx,answer,score = idx_answer_score_corpus[i]
                my_prog_state.update({var_name:f"\"{answer}\""})
                format_step_input = step_input.format(**my_prog_state)
                
                step_output = eval(format_step_input)
                
                if step_output not in predictions_after_eval.keys():
                    predictions_after_eval.update({step_output:score})
                else:
                    predictions_after_eval[step_output] += score
        elif len(eval_vars) == 2:
            var_name_1 = eval_vars[0].strip('{}')
            var_name_2 = eval_vars[1].strip('{}')
            idx_answer_score_corpus_1 = prog_step.state[var_name_1]
            idx_answer_score_corpus_2 = prog_step.state[var_name_2]
            var_name_distribution_1 = prog_step.state[var_name_1+'_distribution']
            var_name_distribution_2 = prog_step.state[var_name_2+'_distribution']
            prog_step.state[output_var+'_distribution'] = [var_name_distribution_1,var_name_distribution_2]

            for i in range(len(idx_answer_score_corpus_1)):
                for j in range(len(idx_answer_score_corpus_2)):
                    my_prog_state = {}
                    idx,answer1,score1 = idx_answer_score_corpus_1[i]
                    idx,answer2,score2 = idx_answer_score_corpus_2[j]
                    my_prog_state.update({var_name_1:f"\"{answer1}\""})
                    my_prog_state.update({var_name_2:f"\"{answer2}\""})
                    format_step_input = step_input.format(**my_prog_state)
                    step_output = eval(format_step_input)

                    score = score1 * score2
                    if step_output not in predictions_after_eval.keys():
                        predictions_after_eval.update({step_output: score})
                    else:
                        predictions_after_eval[step_output] += score
        elif len(eval_vars) == 3:
            var_name_1 = eval_vars[0].strip('{}')
            var_name_2 = eval_vars[1].strip('{}')
            var_name_3 = eval_vars[2].strip('{}')
            idx_answer_score_corpus_1 = prog_step.state[var_name_1]
            idx_answer_score_corpus_2 = prog_step.state[var_name_2]
            idx_answer_score_corpus_3 = prog_step.state[var_name_3]
            var_name_distribution_1 = prog_step.state[var_name_1+'_distribution']
            var_name_distribution_2 = prog_step.state[var_name_2+'_distribution']
            var_name_distribution_3 = prog_step.state[var_name_3+'_distribution']
            prog_step.state[output_var+'_distribution'] = [var_name_distribution_1,var_name_distribution_2, var_name_distribution_3]

            for i in range(len(idx_answer_score_corpus_1)):
                for j in range(len(idx_answer_score_corpus_2)):
                    for p in range(len(idx_answer_score_corpus_3)):
                        my_prog_state = {}
                        idx,answer1,score1 = idx_answer_score_corpus_1[i]
                        idx,answer2,score2 = idx_answer_score_corpus_2[j]
                        idx,answer3,score3 = idx_answer_score_corpus_3[p]
                        my_prog_state.update({var_name_1:f"\"{answer1}\""})
                        my_prog_state.update({var_name_2:f"\"{answer2}\""})
                        my_prog_state.update({var_name_3:f"\"{answer3}\""})
                        format_step_input = step_input.format(**my_prog_state)
                        step_output = eval(format_step_input)

                        score = score1 * score2 * score3
                        if step_output not in predictions_after_eval.keys():
                            predictions_after_eval.update({step_output: score})
                        else:
                            predictions_after_eval[step_output] += score 

        output_eval = []
        
        total_probs = 0
        for key in predictions_after_eval.keys():
            output_eval.append((len(eval_vars), key, predictions_after_eval[key]))
            total_probs += predictions_after_eval[key].item()
        prog_step.state[output_var] = output_eval
        assert abs(total_probs - 1) < 0.0000002
        

        if inspect:
            html_str = ''
            return output_eval, html_str

        return output_eval
    
    def get_eval_var(self,eval_expression):
        matches = re.findall(r'\{[^{}]*\}', eval_expression)
        return list(set(matches))

    def execute_ori(self,prog_step,inspect=False):
        step_input, output_var = self.parse(prog_step)
        prog_state = dict()
        for var_name,var_value in prog_step.state.items():
            if isinstance(var_value,str):
                if var_value.isdecimal():
                    prog_state[var_name] = var_value
                else:
                    prog_state[var_name] = f"'{var_value}'"
            else:
                prog_state[var_name] = var_value
        
        eval_expression = step_input

        if 'xor' in step_input:
            step_input = step_input.replace('xor','!=')

        step_input = step_input.format(**prog_state)
        step_output = eval(step_input)
        prog_step.state[output_var] = step_output
        if inspect:
            html_str = self.html(eval_expression, step_input, step_output, output_var)
            return step_output, html_str

        return step_output


class ResultInterpreter():
    step_name = 'RESULT'

    def __init__(self):
        print(f'Registering {self.step_name} step')

    def parse(self,prog_step):
        parse_result = parse_step(prog_step.prog_str)
        step_name = parse_result['step_name']
        output_var = parse_result['args']['var']
        assert(step_name==self.step_name)
        return output_var

    def html(self,output,output_var):
        step_name = html_step_name(self.step_name)
        output_var = html_var_name(output_var)
        if isinstance(output, Image.Image):
            output = html_embed_image(output,300)
        else:
            output = html_output(output)
            
        return f"""<div>{step_name} -> {output_var} -> {output}</div>"""

    def execute(self,prog_step,inspect=False):
        output_var = self.parse(prog_step)
        output = prog_step.state[output_var]
        if inspect:
            html_str = self.html(output,output_var)
            return [output], html_str

        return [output]


class VQA2Interpreter():
    step_name = 'VQA_internvl'

    def __init__(self,vqa,m_tokenizer):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.vqa = vqa
        self.tokenizer = m_tokenizer
        self.generate_mode = 'rank'
        

    def parse(self,prog_step):
        parse_result = parse_step(prog_step.prog_str)
        step_name = parse_result['step_name']
        args = parse_result['args']
        img_var = args['image']
        question = eval(args['question'])
        output_var = parse_result['output_var']
        return img_var,question,output_var

    def predict(self, img, question):

        temperature = 1.5
        generation_config = dict(
                max_new_tokens=10,
                min_new_tokens=1,
                do_sample=True if temperature > 0 else False,
                temperature=temperature,
                top_p=0.5,
                top_k=50,
                num_return_sequences=10,
                repetition_penalty=1.2,
            )
        
        answers, probs = self.vqa(
            tokenizer=self.tokenizer, 
            img=img, 
            questions=[question], 
            generation_config=generation_config,
        )

        return answers, probs
        

    def html(self,img,question,answer,output_var):
        step_name = html_step_name(self.step_name)
        img_str = html_embed_image(img)
        answer = html_output(answer)
        output_var = html_var_name(output_var)
        image_arg = html_arg_name('image')
        question_arg = html_arg_name('question')
        return f"""<div>{output_var}={step_name}({image_arg}={img_str},&nbsp;{question_arg}='{question}')={answer}</div>"""

    def execute(self, prog_step, inspect=False):
        
        img_var, question, output_var = self.parse(prog_step)

        idx_img_score_corpus = prog_step.state[img_var]

        output_answers = []

        for i in range(len(idx_img_score_corpus)):
            idx, parent_img, parent_score = idx_img_score_corpus[i]
            
            answers, nm_probs = self.predict(parent_img, question)
            if hasattr(parent_score, 'item') and callable(getattr(parent_score, 'item')):
                mul_parent_score = torch.full((nm_probs.size(0), nm_probs.size(1)), parent_score, requires_grad=True).to(torch.device('cuda'))
            else:
                mul_parent_score = torch.full((nm_probs.size(0), nm_probs.size(1)), float(parent_score), requires_grad=True).to(torch.device('cuda'))

            nm_probs = nm_probs * mul_parent_score
            for b in range(nm_probs.size(0)):
                    
                for k in range(len(answers)):
                    output_answers.append((i,answers[k],nm_probs[b][k]))

        prog_step.state[output_var] = output_answers
        prog_step.state[output_var+'_distribution'] = [nm_probs]
        
        if inspect:
            html_str = ''
            return output_answers, html_str

        return output_answers


class LocInterpreter():
    step_name = 'LOC'

    def __init__(self,loc_processor=None, loc_model=None, thresh=0.1,nms_thresh=0.5):
        print(f'Registering {self.step_name} step')
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if loc_processor is None:
            self.processor = None
            self.model = None
            self.processor = OwlViTProcessor.from_pretrained(
                "google/owlvit-large-patch14")
            self.model = OwlViTForObjectDetection.from_pretrained(
                "google/owlvit-large-patch14").to(self.device)
            self.model.eval()
        else:
            self.processor = loc_processor
            self.model = loc_model
        
        self.thresh = thresh
        self.nms_thresh = nms_thresh

    def parse(self,prog_step):
        parse_result = parse_step(prog_step.prog_str)
        step_name = parse_result['step_name']
        img_var = parse_result['args']['image']
        obj_name = eval(parse_result['args']['object'])
        output_var = parse_result['output_var']
        assert(step_name==self.step_name)
        return img_var,obj_name,output_var

    def normalize_coord(self,bbox,img_size):
        w,h = img_size
        x1,y1,x2,y2 = [int(v) for v in bbox]
        x1 = max(0,x1)
        y1 = max(0,y1)
        x2 = min(x2,w-1)
        y2 = min(y2,h-1)
        return [x1,y1,x2,y2]

    def predict(self,img,obj_name):
        encoding = self.processor(
            text=[[f'a photo of {obj_name}']], 
            images=img,
            return_tensors='pt')
        encoding = {k:v.to(self.device) for k,v in encoding.items()}
        with torch.no_grad():
            outputs = self.model(**encoding)
            for k,v in outputs.items():
                if v is not None:
                    outputs[k] = v.to('cpu') if isinstance(v, torch.Tensor) else v
        
        target_sizes = torch.Tensor([img.size[::-1]])
        results = self.processor.post_process(outputs=outputs,target_sizes=target_sizes)
        boxes, scores = results[0]["boxes"], results[0]["scores"]
        boxes = boxes.cpu().detach().numpy().tolist()
        scores = scores.cpu().detach().numpy().tolist()
        if len(boxes)==0:
            raise ValueError("LOC Not Found")
            return []

        boxes, scores = zip(*sorted(zip(boxes,scores),key=lambda x: x[1],reverse=True))
        selected_boxes = []
        selected_scores = []
        
        for i in range(len(scores)):
            if scores[i] > self.thresh:
                coord = self.normalize_coord(boxes[i],img.size)
                selected_boxes.append(coord)
                selected_scores.append(scores[i])
                if len(selected_boxes) >= 1:
                    break 

        selected_boxes, selected_scores = nms(
            selected_boxes,selected_scores,self.nms_thresh)
        nm_scores = selected_scores / np.sum(selected_scores)
        return selected_boxes,nm_scores.tolist()

    def top_box(self,img):
        w,h = img.size        
        return [0,0,w-1,int(h/2)]

    def bottom_box(self,img):
        w,h = img.size
        return [0,int(h/2),w-1,h-1]

    def left_box(self,img):
        w,h = img.size
        return [0,0,int(w/2),h-1]

    def right_box(self,img):
        w,h = img.size
        return [int(w/2),0,w-1,h-1]

    def box_image(self,img,boxes,highlight_best=True):
        img1 = img.copy()
        draw = ImageDraw.Draw(img1)
        for i,box in enumerate(boxes):
            if i==0 and highlight_best:
                color = 'red'
            else:
                color = 'blue'

            draw.rectangle(box,outline=color,width=5)

        return img1

    def html(self,img,box_img,output_var,obj_name):
        step_name=html_step_name(self.step_name)
        obj_arg=html_arg_name('object')
        img_arg=html_arg_name('image')
        output_var=html_var_name(output_var)
        img=html_embed_image(img)
        box_img=html_embed_image(box_img,300)
        return f"<div>{output_var}={step_name}({img_arg}={img}, {obj_arg}='{obj_name}')={box_img}</div>"


    def execute(self,prog_step,inspect=False):
        img_var,obj_name,output_var = self.parse(prog_step)
        parent_img_score_corpus = prog_step.state[img_var]

        loc_output = []
        for i in range(len(parent_img_score_corpus)):
            parent_idx, parent_img, parent_score = parent_img_score_corpus[i]
            if obj_name=='TOP':
                bboxes = [self.top_box(parent_img)]
                scores = [parent_score]
            elif obj_name=='BOTTOM':
                bboxes = [self.bottom_box(parent_img)]
                scores = [parent_score]
            elif obj_name=='LEFT':
                bboxes = [self.left_box(parent_img)]
                scores = [parent_score]
            elif obj_name=='RIGHT':
                bboxes = [self.right_box(parent_img)]
                scores = [parent_score]
            else:
                bboxes, child_scores = self.predict(parent_img,obj_name)
                if len(bboxes) == 0:
                    bboxes = [[]] 
                    scores = [parent_score] 
                else:
                    scores = [parent_score * child_score for child_score in child_scores] 
                
            for bbox, score in zip(bboxes, scores):
                loc_output.append((i, bbox, score))

        prog_step.state[output_var] = loc_output
        
        if inspect:
            html_str = ''

            return loc_output, html_str

        return loc_output


class CountInterpreter():
    step_name = 'COUNT'

    def __init__(self):
        print(f'Registering {self.step_name} step')

    def parse(self,prog_step):
        parse_result = parse_step(prog_step.prog_str)
        step_name = parse_result['step_name']
        box_var = parse_result['args']['box']
        output_var = parse_result['output_var']
        assert(step_name==self.step_name)
        return box_var,output_var

    def html(self,box_img,output_var,count):
        step_name = html_step_name(self.step_name)
        output_var = html_var_name(output_var)
        box_arg = html_arg_name('bbox')
        box_img = html_embed_image(box_img)
        output = html_output(count)
        return f"""<div>{output_var}={step_name}({box_arg}={box_img})={output}</div>"""

    def execute(self,prog_step,inspect=False):
        box_var,output_var = self.parse(prog_step)
        boxes = prog_step.state[box_var]
        count = len(boxes)
        prog_step.state[output_var] = count
        if inspect:
            box_img = prog_step.state[box_var+'_IMAGE']
            html_str = self.html(box_img, output_var, count)
            return count, html_str

        return count


class CropInterpreter():
    step_name = 'CROP'

    def __init__(self):
        print(f'Registering {self.step_name} step')

    def expand_box(self,box,img_size,factor=1.5):
        W,H = img_size
        try:
            x1,y1,x2,y2 = box
        except:
            x1,y1,x2,y2 = 0,0,W,H
        dw = int(factor*(x2-x1)/2)
        dh = int(factor*(y2-y1)/2)
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        x1 = max(0,cx - dw)
        x2 = min(cx + dw,W)
        y1 = max(0,cy - dh)
        y2 = min(cy + dh,H)
        return [x1,y1,x2,y2]

    def parse(self,prog_step):
        parse_result = parse_step(prog_step.prog_str)
        step_name = parse_result['step_name']
        img_var = parse_result['args']['image']
        box_var = parse_result['args']['box']
        output_var = parse_result['output_var']
        assert(step_name==self.step_name)
        return img_var,box_var,output_var

    def html(self,img,out_img,output_var,box_img):
        img = html_embed_image(img)
        out_img = html_embed_image(out_img,300)
        box_img = html_embed_image(box_img)
        output_var = html_var_name(output_var)
        step_name = html_step_name(self.step_name)
        box_arg = html_arg_name('bbox')
        return f"""<div>{output_var}={step_name}({box_arg}={box_img})={out_img}</div>"""

    def execute(self,prog_step,inspect=False):
        img_var,box_var,output_var = self.parse(prog_step)
        idx_img_score_corpus = prog_step.state[img_var]
        idx_box_score_corpus = prog_step.state[box_var]
        
        out_idx_img_score_corpus = []
        
        
        for i in range(len(idx_box_score_corpus)):
            idx, box, score = idx_box_score_corpus[i]
            _,img,_ = idx_img_score_corpus[idx]
            box = self.expand_box(box, img.size)
            out_idx_img_score_corpus.append((idx,img.crop(box),score))

        prog_step.state[output_var] = out_idx_img_score_corpus
        if inspect:
            html_str = ''
            return out_idx_img_score_corpus, html_str

        return out_idx_img_score_corpus


class CropRightOfInterpreter(CropInterpreter):
    step_name = 'CROP_RIGHTOF'

    def right_of(self,box,img_size):
        w,h = img_size
        try:
            x1,y1,x2,y2 = box
        except:
            x1,y1,x2,y2 = 0,0,w,h
        cx = int((x1+x2)/2)
        return [cx,0,w-1,h-1]

    def execute(self,prog_step,inspect=False):

        img_var,box_var,output_var = self.parse(prog_step)
        idx_img_score_corpus = prog_step.state[img_var]
        idx_box_score_corpus = prog_step.state[box_var]
        
        out_idx_img_score_corpus = []
        
        
        for i in range(len(idx_box_score_corpus)):
            idx, box, score = idx_box_score_corpus[i]
            _,img,_ = idx_img_score_corpus[idx]
            box = self.right_of(box, img.size)
            out_idx_img_score_corpus.append((idx,img.crop(box),score))

        prog_step.state[output_var] = out_idx_img_score_corpus
        if inspect:
            # box_img = prog_step.state[box_var+'_IMAGE']
            html_str = ''
            # html_str = self.html(img, out_img, output_var, box_img)
            return out_idx_img_score_corpus, html_str

        return out_idx_img_score_corpus


class CropLeftOfInterpreter(CropInterpreter):
    step_name = 'CROP_LEFTOF'

    def left_of(self,box,img_size):
        w,h = img_size
        try:
            x1,y1,x2,y2 = box
        except:
            x1,y1,x2,y2 = 0,0,w,h
        cx = int((x1+x2)/2)
        return [0,0,cx,h-1]

    def execute(self,prog_step,inspect=False):

        img_var,box_var,output_var = self.parse(prog_step)
        idx_img_score_corpus = prog_step.state[img_var]
        idx_box_score_corpus = prog_step.state[box_var]
        
        out_idx_img_score_corpus = []
        
        for i in range(len(idx_box_score_corpus)):
            idx, box, score = idx_box_score_corpus[i]
            _,img,_ = idx_img_score_corpus[idx]
            box = self.left_of(box, img.size)
            out_idx_img_score_corpus.append((idx,img.crop(box),score))

        prog_step.state[output_var] = out_idx_img_score_corpus
        if inspect:
            html_str = ''
            return out_idx_img_score_corpus, html_str

        return out_idx_img_score_corpus


class CropAboveInterpreter(CropInterpreter):
    step_name = 'CROP_ABOVE'

    def above(self,box,img_size):
        w,h = img_size
        try:
            x1,y1,x2,y2 = box
        except:
            x1,y1,x2,y2 = 0,0,w,h
        cy = int((y1+y2)/2)
        return [0,0,w-1,cy]

    def execute(self,prog_step,inspect=False):
        
        img_var,box_var,output_var = self.parse(prog_step)
        idx_img_score_corpus = prog_step.state[img_var]
        idx_box_score_corpus = prog_step.state[box_var]
        
        out_idx_img_score_corpus = []
        
        for i in range(len(idx_box_score_corpus)):
            idx, box, score = idx_box_score_corpus[i]
            _,img,_ = idx_img_score_corpus[idx]
            box = self.above(box, img.size)
            out_idx_img_score_corpus.append((idx,img.crop(box),score))

        prog_step.state[output_var] = out_idx_img_score_corpus
        if inspect:
            html_str = ''
            return out_idx_img_score_corpus, html_str

        return out_idx_img_score_corpus


class CropBelowInterpreter(CropInterpreter):
    step_name = 'CROP_BELOW'

    def below(self,box,img_size):
        w,h = img_size
        try:
            x1,y1,x2,y2 = box
        except:
            x1,y1,x2,y2 = 0,0,w,h
        cy = int((y1+y2)/2)
        return [0,cy,w-1,h-1]

    def execute(self,prog_step,inspect=False):

        img_var,box_var,output_var = self.parse(prog_step)
        idx_img_score_corpus = prog_step.state[img_var]
        idx_box_score_corpus = prog_step.state[box_var]
        
        out_idx_img_score_corpus = []
        
        for i in range(len(idx_box_score_corpus)):
            idx, box, score = idx_box_score_corpus[i]
            _,img,_ = idx_img_score_corpus[idx]
            box = self.below(box, img.size)
            out_idx_img_score_corpus.append((idx,img.crop(box),score))

        prog_step.state[output_var] = out_idx_img_score_corpus
        if inspect:
            html_str = ''
            return out_idx_img_score_corpus, html_str

        return out_idx_img_score_corpus


class CropFrontOfInterpreter(CropInterpreter):
    step_name = 'CROP_FRONTOF'


class CropInFrontInterpreter(CropInterpreter):
    step_name = 'CROP_INFRONT'


class CropInFrontOfInterpreter(CropInterpreter):
    step_name = 'CROP_INFRONTOF'


class CropBehindInterpreter(CropInterpreter):
    step_name = 'CROP_BEHIND'


class CropAheadInterpreter(CropInterpreter):
    step_name = 'CROP_AHEAD'


def register_step_interpreters(dataset, vqa, m_tokenizer, loc_processor=None, loc_model=None):
    if dataset != 'gqa':
        raise ValueError(f'Unsupported dataset: {dataset!r}; only gqa is supported')
    return dict(
        LOC=LocInterpreter(loc_processor, loc_model),
        COUNT=CountInterpreter(),
        CROP=CropInterpreter(),
        CROP_RIGHTOF=CropRightOfInterpreter(),
        CROP_LEFTOF=CropLeftOfInterpreter(),
        CROP_FRONTOF=CropFrontOfInterpreter(),
        CROP_INFRONTOF=CropInFrontOfInterpreter(),
        CROP_INFRONT=CropInFrontInterpreter(),
        CROP_BEHIND=CropBehindInterpreter(),
        CROP_AHEAD=CropAheadInterpreter(),
        CROP_BELOW=CropBelowInterpreter(),
        CROP_ABOVE=CropAboveInterpreter(),
        VQA=VQA2Interpreter(vqa, m_tokenizer),
        EVAL=EvalInterpreter(),
        RESULT=ResultInterpreter()
    )
