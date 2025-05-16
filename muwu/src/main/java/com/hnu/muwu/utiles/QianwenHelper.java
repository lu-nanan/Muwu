package com.hnu.muwu.utiles;

import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class QianwenHelper {
    public static String processMessage(String userMessage)
            throws NoApiKeyException, ApiException, InputRequiredException {

        // 每次调用都创建新的消息列表，不保留历史
        List<Message> messages = new ArrayList<>();
        // 添加系统提示
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        messages.add(systemMsg);

        // 添加当前用户消息
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(userMessage)
                .build();
        messages.add(userMsg);

        // 调用API生成响应
        Generation gen = new Generation();
        GenerationParam param = GenerationParam.builder()
                .model("qwen-max")
                .messages(messages)
                .apiKey("sk-d5f513233df44e37b00ac124cb589492")
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .topP(0.8)
                .build();
        GenerationResult result = gen.call(param);

        // 直接返回结果内容，不保留历史
        return result.getOutput().getChoices().get(0).getMessage().getContent();
    }

    public static void main(String[] args) {
        try {
            String response1 = processMessage("你好");
            System.out.println("Qwen: " + response1);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}