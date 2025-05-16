package com.hnu.muwu.utiles;

import org.springframework.stereotype.Component;

import java.util.HashMap;

@Component
public class TranslateHelper {

    public static String translate(String text) {
        String question = "请将下面的英文翻译成中文，回答直接输出翻译结果，不可有其他任何无关的内容\n" + text;
        try {
            return QianwenHelper.processMessage(question);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            return e.getMessage();
        }
    }
}
