---
layout: post
title: "JsonToSoql"
date: 2023-07-29 00:02:00 +0800
categories: java
--- 
 
{% highlight java %}

import java.io.*;
import java.util.Stack;

public class JsonToSoql {
    private String inputFile = "d:/temp/3.json";

    class Condition {
        String field = "";
        String operator = "";
        String values = "";
    }

    public String analyze() throws IOException {
        BufferedReader  br = new BufferedReader(new FileReader(inputFile));
        String line = null;
        Stack<String> stack = new Stack<>();
        StringBuilder result = new StringBuilder();
        Condition condition = null;

        while ((line = br.readLine()) != null) {
            System.out.println(line);

            if (line.contains("\"conditions\"")) {
                stack.push("(");
            }

            if (line.contains("\"field\"") || line.contains("\"operator\"") ||line.contains("\"values\"")) {
                if(condition == null ){
                    condition = new Condition();
                }
                condition = setCondition(line, condition);

                if (isConditionDone(condition)){
                    String condStr = String.format("(%s %s %s)", condition.field, condition.operator, condition.values);
                    stack.push(condStr);
                    condition = null;
                }
            }

            if (line.contains("conjunction")) {
                String[] arr = line.split(":");
                String value = arr[1].split("\"")[1];
                String condStr = "";
                Stack<String> condStack = new Stack<>();
                StringBuilder currentConj = new StringBuilder();

                while (!(condStr = stack.pop()).equals("(")) {
                    condStack.push(condStr);
                }

                while (condStack.size() > 0) {
                    condStr =condStack.pop();
                    currentConj.append(condStr);

                    if (condStack.size()>=1) {
                        currentConj.append(String.format(" %s ",value));
                    }
                }
                stack.push(String.format("(%s)" , currentConj));
            }

        }
        br.close();

        return stack.pop();
    }

    private boolean isConditionDone(Condition cond) {
        return !cond.operator.isEmpty() && !cond.field.isEmpty() && !cond.values.isEmpty() ;
    }

    private Condition setCondition(String line, Condition cond) {
        String[] arr = line.split(":");
        String value = arr[1].split(",")[0].replaceAll("\"", "").trim();

        if (line.contains("\"field\"")) {
            cond.field = value;
        }
        if (line.contains("\"operator\"")) {
            cond.operator = value;

            // todo: operator conversion
//            if (cond.operator.startsWith("not")) {
//                cond.field = "not " + cond.field;
//                cond.operator = cond.operator.substring(3);
//            }
        }

        if (line.contains("\"values\"")) {
            cond.values = value
                    .replaceAll("\\[", "")
                    .replaceAll("]", "");
        }

        return cond;
    }

    public static void main(String[] args) {
        try {
            String result = new JsonToSoql().analyze();
            System.out.println(result);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
{% endhighlight %}