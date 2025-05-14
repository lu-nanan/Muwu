package com.hnu.muwu.utiles;

import com.rabbitmq.client.*;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.concurrent.atomic.AtomicReference;

@Component
public class MessageQueueHelper {

    // RabbitMQ连接参数
    private static final String host = "localhost";
    private static final int port = 5672;
    private static final String virtualHost = "/";
    private static final String username = "admin";
    private static final String password = "123456";
    private static final String exchangeName = "python-test";

    private static Connection connection;
    private static Channel channel;
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public MessageQueueHelper() throws IOException, TimeoutException {
        if (connection == null || !connection.isOpen() ||
                channel == null || !channel.isOpen()) {
            connect();
        }
    }

    private static void connect() throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(host);
        factory.setPort(port);
        factory.setVirtualHost(virtualHost);
        factory.setUsername(username);
        factory.setPassword(password);

        connection = factory.newConnection();
        channel = connection.createChannel();

        // 声明fanout类型exchange
        channel.exchangeDeclare(exchangeName, BuiltinExchangeType.FANOUT, true);
    }

    /**
     * 发送消息并等待结果
     * @param filePath 文件路径
     * @param operation 操作类型
     * @return Python处理后的结果（已解析为Map）
     * @throws IOException
     * @throws TimeoutException
     * @throws InterruptedException
     */
    public static Map<String, Object> sendMessageAndGetResult(String filePath, String operation)
            throws IOException, TimeoutException, InterruptedException {

        if (connection == null || !connection.isOpen() ||
                channel == null || !channel.isOpen()) {
            connect();
        }

        // 创建临时回调队列
        String callbackQueue = channel.queueDeclare().getQueue();

        // 设置消息属性（指定回复队列）
        AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                .replyTo(callbackQueue)
                .build();

        // 构造消息体
        Map<String, Object> message = new HashMap<>();
        message.put("file_path", filePath);
        message.put("operation", operation);

        String jsonMessage = toJson(message);

        // 用于同步等待结果的对象
        final Object monitor = new Object();
        final AtomicReference<String> result = new AtomicReference<>(null);

        // 设置消费者监听回调队列
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String response = new String(delivery.getBody(), StandardCharsets.UTF_8);
            System.out.println("Python处理结果 (原始JSON): " + response);
            result.set(response);

            // 通知等待线程已收到结果
            synchronized (monitor) {
                monitor.notify();
            }
        };

        String consumerTag = channel.basicConsume(callbackQueue, true, deliverCallback, consumerTag1 -> {});

        // 发布消息到exchange
        channel.basicPublish(exchangeName, "", props, jsonMessage.getBytes(StandardCharsets.UTF_8));
        System.out.println("消息已发送: " + jsonMessage);

        // 等待结果（设置超时）
        synchronized (monitor) {
            monitor.wait(10000); // 10秒超时
        }

        // 取消消费者
        channel.basicCancel(consumerTag);

        // 解析JSON响应为Map
        if (result.get() != null) {
            try {
                Map<String, Object> resultMap = objectMapper.readValue(result.get(), Map.class);

                // 打印解码后的结果
                System.out.println("Python处理结果 (解码后): ");
                resultMap.forEach((key, value) -> System.out.println(key + ": " + value));

                return resultMap;
            } catch (Exception e) {
                System.err.println("解析JSON响应失败: " + e.getMessage());
                return null;
            }
        }

        return null;
    }

    /**
     * 将Map转换为JSON字符串
     * @param map 数据Map
     * @return JSON字符串
     */
    private static String toJson(Map<String, Object> map) {
        try {
            return objectMapper.writeValueAsString(map);
        } catch (Exception e) {
            // 如果Jackson序列化失败，回退到手动构建JSON
            StringBuilder json = new StringBuilder("{");
            for (Map.Entry<String, Object> entry : map.entrySet()) {
                if (json.length() > 1) json.append(",");
                json.append("\"").append(entry.getKey()).append("\":\"");
                json.append(entry.getValue()).append("\"");
            }
            json.append("}");
            return json.toString();
        }
    }

    /**
     * 关闭连接和channel
     */
    public static void close() throws IOException, TimeoutException {
        if (channel != null && channel.isOpen()) {
            channel.close();
        }
        if (connection != null && connection.isOpen()) {
            connection.close();
        }
    }

    public static void main(String[] args) {
        try {
            // 示例：发送文件处理请求
            String filePath = "F:/大三下学期/移动应用开发/仓库/Muwu/image.png";  // 替换为实际文件路径
            String operation = "OCR";

            Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(filePath, operation);

            if (result != null) {
                String status = (String) result.get("status");
                String resultPath = (String) result.get("result");

                System.out.println("\n处理状态: " + status);
                System.out.println("结果文件路径: " + resultPath);
            } else {
                System.out.println("未收到处理结果或处理超时");
            }

            // 关闭连接
            MessageQueueHelper.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}