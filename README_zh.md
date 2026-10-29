# eDoT

**End-to-End Differentiable Optimization of Tool-Augmented Visual Reasoning via Probabilistic Graphs**

Wentao Wan, Kaiyu Wu, Qingyang Ma, Nan Kang, Yunjie Chen, Liang Lin, Keze Wang

**Findings of EMNLP 2026** | [论文](https://aclanthology.org/2026.findings-emnlp.2444/)

[English](README.md) | **简体中文**

## 项目介绍

eDoT 通过概率化程序执行优化视觉程序中的工具模型：将中间答案表示为候选概率，按照程序逻辑组合，利用最终任务标签构建损失，使梯度能够回传到被调用的 VQA 模型。

![eDoT 方法流程图](assets/pipeline.png)

## 代码结构

| 模块 | 源码 | 作用 |
|---|---|---|
| 程序执行 | [utils.py](visprog/engine/utils.py) | `Program` 与 `ProgramInterpreter`：维护程序状态、调度各执行步骤。 |
| 概率传播 | [step_interpreters.py](visprog/engine/step_interpreters.py) | 视觉工具调用、图像裁剪、EVAL 概率聚合与 RESULT 输出。 |
| 训练连接 | [run_code.py](visprog/run_code.py) | 通过 `get_result_supervised` 将训练样本接入程序执行。 |
| 模型与损失 | [modeling_internvl_chat.py](internvl/model/internvl_chat/modeling_internvl_chat.py) | InternVL 候选答案评分、最终答案损失与 LLM LoRA。 |
| 数据处理 | [train/](internvl/train/) · [pad_data_collator.py](internvl/patch/pad_data_collator.py) | 图像与文本预处理，将程序和最终任务标签传递给模型。 |
| 提示词 | [prompt.py](data_process/prompt.py) · [回退模板](visprog/prompts/gqa_fixed_code.prompt) | 原始程序生成提示词，以及单步 VQA 异常回退模板。 |

主要训练调用关系：

```text
训练样本 → InternVL forward → ProgramInterpreter
         → VQA 候选评分 → EVAL / RESULT → 最终答案损失
```

## 源码使用方式

1. 准备配套的 **InternVL1.5 / VisProg 环境**和 Mini-InternVL-Chat-2B-V1-5 权重。
2. 将 `internvl/` 中的文件放入上游 `InternVL/internvl_chat/internvl/` 下的同名位置，将 `visprog/` 放在 `InternVL/internvl_chat/` 下。
3. 在原训练配置中设置权重、标注和图像路径。

## 致谢与许可

- 程序执行和裁剪代码基于 [VisProg](https://github.com/allenai/visprog)。
- 模型与预处理代码基于 [InternVL](https://github.com/OpenGVLab/InternVL)。

## 引用

如果本代码对你的研究有所帮助，请引用上述 eDoT 论文，并注明所使用的上游项目。

```bibtex
@inproceedings{wan-etal-2026-end,
    title = "End-to-End Differentiable Optimization of Tool-Augmented Visual Reasoning via Probabilistic Graphs",
    author = "Wan, Wentao and Wu, Kaiyu and Ma, Qingyang and Kang, Nan and Chen, Yunjie and Lin, Liang and Wang, Keze",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {EMNLP} 2026",
    year = "2026",
    pages = "52467--52482",
}
```
