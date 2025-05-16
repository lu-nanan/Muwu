package com.hnu.muwu.utiles;

import org.springframework.stereotype.Component;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

@Component
public class FileTreeHelper {

    private static final String LINE_PREFIX = "│   ";
    private static final String BRANCH_PREFIX = "├── ";
    private static final String LAST_BRANCH_PREFIX = "└── ";

    /**
     * 生成文件树字符串表示
     * @param directoryPath 目标文件夹路径
     * @return 文件树的字符串表示
     */
    public static String generateFileTree(String directoryPath) {
        File root = new File(directoryPath);
        if (!root.exists()) {
            return "指定路径不存在: " + directoryPath;
        }

        if (!root.isDirectory()) {
            return "指定路径不是文件夹: " + directoryPath;
        }

        StringBuilder treeBuilder = new StringBuilder();
        treeBuilder.append(root.getName()).append("/\n");
        generateFileTreeInternal(root, "", treeBuilder);

        return treeBuilder.toString();
    }

    /**
     * 递归生成文件树
     * @param directory 当前处理的文件夹
     * @param prefix 当前行的前缀
     * @param treeBuilder 构建文件树的StringBuilder
     */
    private static void generateFileTreeInternal(File directory, String prefix, StringBuilder treeBuilder) {
        File[] files = directory.listFiles();
        if (files == null) {
            return;
        }

        List<File> fileList = new ArrayList<>();
        List<File> dirList = new ArrayList<>();

        for (File file : files) {
            if (file.isDirectory()) {
                dirList.add(file);
            } else {
                fileList.add(file);
            }
        }

        dirList.sort((f1, f2) -> f1.getName().compareToIgnoreCase(f2.getName()));
        fileList.sort((f1, f2) -> f1.getName().compareToIgnoreCase(f2.getName()));

        List<File> sortedFiles = new ArrayList<>();
        sortedFiles.addAll(dirList);
        sortedFiles.addAll(fileList);

        for (int i = 0; i < sortedFiles.size(); i++) {
            File file = sortedFiles.get(i);
            boolean isLast = (i == sortedFiles.size() - 1);

            String currentPrefix = isLast ? LAST_BRANCH_PREFIX : BRANCH_PREFIX;

            treeBuilder.append(prefix).append(currentPrefix).append(file.getName());
            if (file.isDirectory()) {
                treeBuilder.append("/");
            }
            treeBuilder.append("\n");

            if (file.isDirectory()) {
                String newPrefix = prefix + (isLast ? "    " : LINE_PREFIX);
                generateFileTreeInternal(file, newPrefix, treeBuilder);
            }
        }
    }

    public static void main(String[] args) {
        try {
            String directoryPath = "F:/大三下学期/移动应用开发/仓库/Muwu";  // 替换为实际文件夹路径
            String fileTree = FileTreeHelper.generateFileTree(directoryPath);
            System.out.println(fileTree);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}