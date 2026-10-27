throw new Error('Historical session archive: execution is disabled pending approved synthetic inputs and compatible dependencies.');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
        HeadingLevel } = require('docx');
const fs = require('fs');

const outputPath = '<configured-input>';

// A4 page
const pageSize = { width: 11906, height: 16838 };

// Border style
const border = { style: BorderStyle.SINGLE, size: 6, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 100, bottom: 100, left: 120, right: 120 };

// 6 columns totaling 9000 DXA
const COL = [1300, 1700, 1300, 1700, 1300, 1700];

// Helper: label cell with center alignment, supports red hint text
function labelCell(text, redHint, colIndex) {
    const children = [new TextRun({ text, font: "宋体" })];
    if (redHint) {
        children.push(new TextRun({ text: redHint, color: "FF0000", font: "宋体" }));
    }
    return new TableCell({
        borders,
        width: { size: COL[colIndex], type: WidthType.DXA },
        margins: cellMargins,
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children
        })]
    });
}

// Helper: empty input cell
function emptyCell(colIndex, opts = {}) {
    return new TableCell({
        borders,
        width: { size: COL[colIndex], type: WidthType.DXA },
        margins: cellMargins,
        verticalAlign: opts.vAlign || VerticalAlign.CENTER,
        children: [new Paragraph({ children: [new TextRun("")] })]
    });
}

// Helper: empty input cell that spans multiple columns
function emptyCellSpan(colSpan, opts = {}) {
    return new TableCell({
        borders,
        columnSpan: colSpan,
        width: { size: COL.slice(1, 1 + colSpan).reduce((a, b) => a + b, 0), type: WidthType.DXA },
        margins: cellMargins,
        verticalAlign: opts.vAlign || VerticalAlign.TOP,
        children: [new Paragraph({ children: [new TextRun("")] })]
    });
}

// Helper: label cell that spans multiple columns
function labelCellSpan(text, colSpan, colIndex, opts = {}) {
    const children = [new TextRun({ text, font: "宋体" })];
    if (opts.redHint) {
        children.push(new TextRun({ text: opts.redHint, color: "FF0000", font: "宋体" }));
    }
    return new TableCell({
        borders,
        columnSpan: colSpan,
        width: { size: COL.slice(colIndex, colIndex + colSpan).reduce((a, b) => a + b, 0), type: WidthType.DXA },
        margins: cellMargins,
        verticalAlign: opts.vAlign || VerticalAlign.CENTER,
        children: [new Paragraph({
            alignment: opts.alignment || AlignmentType.CENTER,
            children
        })]
    });
}

// Build the table rows
const tableRows = [
    // Row 1: 学院 | 班级 | 实践服务单位
    new TableRow({
        height: { value: 700, rule: 'atLeast' },
        children: [
            labelCell("学院", "(需写全称)", 0),
            emptyCell(1),
            labelCell("班级", "(需写全称)", 2),
            emptyCell(3),
            labelCell("实践服务单位\n(公章)", null, 4),
            emptyCell(5)
        ]
    }),
    // Row 2: 姓名 | 实践学时
    new TableRow({
        height: { value: 700, rule: 'atLeast' },
        children: [
            labelCell("姓名", null, 0),
            emptyCell(1),
            labelCell("实践学时", "(以\"小时或天\"为单位)", 2),
            emptyCell(3),
            labelCell("", null, 4),
            emptyCell(5)
        ]
    }),
    // Row 3: 学号 (spans 5 cols)
    new TableRow({
        height: { value: 700, rule: 'atLeast' },
        children: [
            labelCell("学号", "(需为完整学号)", 0),
            emptyCellSpan(5, { vAlign: VerticalAlign.CENTER })
        ]
    }),
    // Row 4: 活动内容及成果 (spans 5 cols, tall)
    new TableRow({
        height: { value: 5500, rule: 'atLeast' },
        children: [
            new TableCell({
                borders,
                width: { size: COL[0], type: WidthType.DXA },
                margins: cellMargins,
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [
                        new TextRun({ text: "活动内容\n及成果", font: "宋体" }),
                        new TextRun({ text: "（不少于500字）", color: "FF0000", font: "宋体" })
                    ]
                })]
            }),
            emptyCellSpan(5, { vAlign: VerticalAlign.TOP })
        ]
    }),
    // Row 5: 评分 | 任课教师
    new TableRow({
        height: { value: 700, rule: 'atLeast' },
        children: [
            labelCell("评分", null, 0),
            emptyCell(1),
            labelCell("任课教师\n签名", null, 2),
            emptyCell(3),
            labelCell("", null, 4),
            emptyCell(5)
        ]
    })
];

const table = new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: COL,
    rows: tableRows
});

const doc = new Document({
    styles: {
        default: { document: { run: { font: "宋体", size: 24 } } }
    },
    sections: [{
        properties: {
            page: {
                size: pageSize,
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        children: [
            // 附件5
            new Paragraph({
                alignment: AlignmentType.LEFT,
                spacing: { before: 0, after: 200 },
                children: [new TextRun({ text: "附件5", font: "宋体", size: 24 })]
            }),
            // 标题
            new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { before: 0, after: 100 },
                children: [new TextRun({ text: "合成示例段落：用于验证文档布局与内容转换流程", font: "宋体", size: 32, bold: true })]
            }),
            // 学期
            new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { before: 0, after: 300 },
                children: [new TextRun({ text: "（2025—2026学年第二学期）", font: "宋体", size: 24 })]
            }),
            // 表格
            table,
            // 备注
            new Paragraph({
                alignment: AlignmentType.LEFT,
                spacing: { before: 300, after: 0 },
                children: [
                    new TextRun({ text: "备注：", bold: true, font: "宋体", size: 24 }),
                    new TextRun({ text: "1.成绩评定按百分制计算；", font: "宋体", size: 24 })
                ]
            }),
            new Paragraph({
                alignment: AlignmentType.LEFT,
                spacing: { before: 0, after: 0 },
                indent: { left: 540 },
                children: [
                    new TextRun({ text: "2.打印时删除", font: "宋体", size: 24 }),
                    new TextRun({ text: "“备注”", color: "FF0000", font: "宋体", size: 24 }),
                    new TextRun({ text: "和", font: "宋体", size: 24 }),
                    new TextRun({ text: "红色部分", color: "FF0000", font: "宋体", size: 24 }),
                    new TextRun({ text: "的说明。", font: "宋体", size: 24 })
                ]
            })
        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputPath, buffer);
    console.log("Word document created at: " + outputPath);
});
