from .step_interpreters import register_step_interpreters, parse_step


class Program:
    def __init__(self,prog_str,init_state=None):
        self.prog_str = prog_str
        self.state = init_state if init_state is not None else dict()
        self.instructions = self.prog_str.split('\n')


class ProgramInterpreter:
    def __init__(self,dataset, vqa, m_tokenizer, loc_processor=None, loc_model=None):
        self.step_interpreters = register_step_interpreters(dataset,vqa, m_tokenizer, loc_processor, loc_model)

    def execute_step(self,prog_step,inspect):
        step_name = parse_step(prog_step.prog_str,partial=True)['step_name']

        if step_name in self.step_interpreters:
            return self.step_interpreters[step_name].execute(prog_step, inspect)
        else:
            print(f"Error: Step {step_name} is not supported")
            return None, None if inspect else None
        
    def execute(self,prog,init_state,inspect=False):
        if isinstance(prog,str):
            prog = Program(prog,init_state)
        else:
            assert(isinstance(prog,Program))

        prog_steps = [Program(instruction,init_state=prog.state) \
            for instruction in prog.instructions]

        html_str = '<hr>'
        for prog_step in prog_steps:
            if inspect:
                step_output, step_html = self.execute_step(prog_step,inspect)
                html_str += step_html + '<hr>'
            else:
                step_output = self.execute_step(prog_step,inspect)
            if step_output == "EVALexecute_error":
                return "EVALexecute_error",None,None
            if step_output == "VQAexecute_error":
                return "VQAexecute_error",None,None

        if inspect:
            return step_output, prog.state, html_str

        return step_output, prog.state
