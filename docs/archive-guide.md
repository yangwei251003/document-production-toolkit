# 历史脚本与运行条件（v0.1的35个版本）

本页保留v0.1的35个来源版本；本轮新增20个会话程序见[会话增补](session-guide.md)。原有函数、循环、分支和异常控制流保留；变更集中于敏感字面量、合成文案、工作目录绑定与默认执行阻断。原始材料、照片、证件、外部模板与AI生成原图未打包。

`python -m document_toolkit demo` 只启用经过验证的四变体简历生成流程。其他档案保留源码供研究/改造，需自备有权使用的输入、适配路径并审查副作用。Office、联网抓取、素材整理/移动等档案默认阻断，不能将源码保存解释为所有历史工作流已经实跑。

| 来源版本 | 类别 | 主要依赖 |
| --- | --- | --- |
| `career/assemble_ppt_delivery.py` | document-workflow | pypdf, python-pptx, reportlab |
| `career/assemble_v2.py` | document-workflow | pypdf, python-pptx, reportlab |
| `career/build_ppt_review.py` | document-workflow |  |
| `career/build_resumes.py` | document-workflow | python-docx |
| `career/export_word.ps1` | office |  |
| `career/fetch_ppt_references.py` | network | lxml, requests |
| `career/finalize_honors.py` | document-workflow | Pillow |
| `career/finalize_ppt_delivery.py` | document-workflow | Pillow |
| `career/finalize_v2.py` | document-workflow | Pillow |
| `career/package_delivery.py` | document-workflow |  |
| `career/prepare_ppt_generation.py` | document-workflow |  |
| `career/prepare_v2.py` | document-workflow |  |
| `career/record_ppt_image.py` | document-workflow | Pillow |
| `career/record_v2_image.py` | document-workflow | Pillow |
| `career/render_and_check.py` | document-workflow | pdfplumber, python-docx |
| `career/revision_assets.py` | network | beautifulsoup4, requests |
| `career/revision_download_selected.py` | network | requests |
| `career/update_honors.py` | document-workflow | Pillow, pypdf, python-pptx, reportlab |
| `career/verify_ppt_native.ps1` | office |  |
| `career/verify_v2_native.ps1` | office |  |
| `scholarship/国家奖学金申请表_填写版/01_转换并导出.ps1` | office |  |
| `scholarship/国家奖学金申请表_填写版/02_生成两页申请表.py` | document-workflow | python-docx |
| `scholarship/国家奖学金申请表_填写版/03_结构与内容校验.py` | document-workflow | python-docx |
| `scholarship/国家奖学金申请表_填写版/04_按原格式去除修订并转DOCX.py` | office | pywin32 |
| `scholarship/国家奖学金答辩_修订版/生成与检查记录/render_sources.py` | document-workflow | Pillow, playwright |
| `scholarship/国家奖学金答辩_修订版/生成与检查记录/打包交付.py` | document-workflow | Pillow, PyMuPDF, python-pptx |
| `scholarship/国家奖学金答辩_最终版/制作记录/assemble_final.py` | document-workflow | Pillow, PyMuPDF, playwright, python-pptx |
| `scholarship/国家奖学金答辩_最终版/制作记录/verify_final.py` | document-workflow | Pillow, PyMuPDF, python-pptx |
| `scholarship/整理说明与索引/工具/add_new.py` | document-workflow | Pillow |
| `scholarship/整理说明与索引/工具/build_16page_plan.py` | document-workflow |  |
| `scholarship/整理说明与索引/工具/organize.py` | organizer | Pillow |
| `scholarship/整理说明与索引/工具/organize_round3.py` | organizer | Pillow |
| `scholarship/整理说明与索引/工具/prepare.py` | document-workflow | Pillow |
| `scholarship/整理说明与索引/工具/read_video.py` | document-workflow | Pillow, imageio-ffmpeg, opencv-python |
| `scholarship/整理说明与索引/工具/update_context.py` | document-workflow | Pillow |

完整的来源相对路径、原始SHA256、公开副本SHA256与控制流统计见 `source-map.json`。原件绝对路径仅留在本机私有审计清单中。共发现2组结构相近版本，全部保留差异，不把文本或输入不同的程序草率覆盖。

本轮只验证了Python/PowerShell语法、默认阻断与合成DOCX子流程。未执行真实Word/PowerPoint、原始文档处理、视频读取、网络下载、文件移动或清理；ReportLab/pdfplumber等历史依赖本机亦未安装。
