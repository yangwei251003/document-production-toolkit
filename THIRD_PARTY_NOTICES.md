# 第三方依赖与素材

本仓库原创脚本、适配器与几何占位图采用 MIT。依赖的软件许可独立适用；仓库不捆绑依赖包、Office程序、字体、第三方照片或原始个人材料。

| 用途 | 依赖 | 许可/来源 |
| --- | --- | --- |
| 已运行的 DOCX 示例 | python-docx 1.1.2 | MIT；https://github.com/python-openxml/python-docx |
| 已运行的合成几何图 | Pillow 11.0.0 | MIT-CMU；https://github.com/python-pillow/Pillow |
| DOCX依赖 | lxml | BSD-3-Clause；https://github.com/lxml/lxml |
| 历史PPT源码可选 | python-pptx | MIT；https://github.com/scanny/python-pptx |
| 历史PDF源码可选 | pypdf / ReportLab / pdfplumber | 各项目 BSD / BSD / MIT；https://github.com/py-pdf/pypdf 、https://www.reportlab.com/ 、https://github.com/jsvine/pdfplumber |
| 历史PDF源码可选 | PyMuPDF（fitz/pymupdf） | AGPL-3.0 或商业许可；https://github.com/pymupdf/PyMuPDF 。使用或分发相关组合程序时须遵循该依赖许可，不能将其称作MIT依赖。 |
| 历史浏览器源码可选 | Playwright | Apache-2.0；https://github.com/microsoft/playwright-python |
| 历史抓取源码可选 | requests / BeautifulSoup | Apache-2.0 / MIT；https://github.com/psf/requests 、https://www.crummy.com/software/BeautifulSoup/ |
| 历史视频源码可选 | OpenCV / imageio-ffmpeg | Apache-2.0 / BSD-2-Clause；实际FFmpeg二进制许可取决于发行构建，未捆绑。 |
| 历史Office源码可选 | pywin32 / Microsoft Office | pywin32为PSF；Office是另行许可的专有软件，未捆绑、未运行。 |

主要已用依赖的原始许可文本及哈希见 `third-party/`。Microsoft YaHei、Arial 等字体仅为样式名称，未复制字体文件。历史脚本保留的公共参考URL是输入来源说明，不代表取得图片或文档再分发许可；抓取和图片素材未包含在示例中。

`fixture-portrait.png` 是本项目通过Pillow绘制的几何占位图，不是真人照片。README截图是本项目合成示例的实际运行页面，不是原始简历/奖学金材料截图。

## 0.2 会话源码增补

合成工作簿实际使用 openpyxl 3.1.5（MIT）及 et-xmlfile（MIT），原始许可文本见third-party/licenses；没有捆绑这些运行库。

`create_form.js` 调用标准 npm `docx` 与Node内建`fs`。当前上游docx为MIT（https://github.com/dolanmiu/docx/blob/master/LICENSE），原会话没有提供版本锁文件，因此仅验证Node语法，未安装该依赖或声称完整复建。

本批未发现私有平台运行库导入；无法复现的条件具体是原模板/素材/资料未公开、Office未运行及旧npm依赖版本未锁定。没有复制原文章、财务工作簿、签名图片、商业字体或平台私有运行库。阅读器模板中的长文案和报告正文已换成合成fixture，原程序的HTML/JavaScript模板结构与纯转换函数保留。
