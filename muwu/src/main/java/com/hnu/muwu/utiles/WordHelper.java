package com.hnu.muwu.utiles;

import org.apache.poi.xwpf.extractor.XWPFWordExtractor;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.springframework.stereotype.Component;

import java.io.FileInputStream;
import java.io.IOException;

@Component
public class WordHelper {

    /**
     * 读取指定路径的 .docx 文档内容，并以纯文本形式返回
     *
     * @param filePath .docx 文件的绝对路径或相对路径
     * @return 文档中的所有文本内容（按段落拼接）
     * @throws IOException 当文件无法打开或读取时抛出
     */
    public static String readDocx(String filePath) throws IOException {
        try (FileInputStream fis = new FileInputStream(filePath);
             XWPFDocument document = new XWPFDocument(fis);
             XWPFWordExtractor extractor = new XWPFWordExtractor(document)) {

            // 直接使用 XWPFWordExtractor 提取文档中的全部文本
            return extractor.getText();
        }
    }

    /**
     * 将 .docx 文档按段落一行一行打印出来
     *
     * @param filePath .docx 文件的路径
     * @throws IOException 当文件无法打开或读取时抛出
     */
    public static void printDocxByParagraph(String filePath) throws IOException {
        try (FileInputStream fis = new FileInputStream(filePath);
             XWPFDocument document = new XWPFDocument(fis)) {

            // 遍历所有段落并逐行打印
            document.getParagraphs().forEach(paragraph -> {
                System.out.println(paragraph.getText());
            });
        }
    }

    /**
     * 示例演示了如何调用 readDocx 和 printDocxByParagraph 方法进行文档内容读取
     */
    public static void main(String[] args) {
        String filePath = "F:\\大三下学期\\个人文件\\（20230509更新）党员发展材料模板参考（全）\\6.入党积极分子培养考察表写法.docx";

        try {
            // 1. 读取整个文档为一个大字符串
            String content = readDocx(filePath);
            System.out.println("=== 文档全文（纯文本） ===");
            System.out.println(content);

            System.out.println("\n=== 按段落逐行打印 ===");
            // 2. 按段落打印
            printDocxByParagraph(filePath);

        } catch (IOException e) {
            System.err.println("读取 .docx 文档时发生异常： " + e.getMessage());
            e.printStackTrace();
        }
    }
}