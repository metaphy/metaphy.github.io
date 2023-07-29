---
layout: post
title: "将JSON格式的条件转为SQL的where条件"
date: 2023-07-29 00:02:00 +0800
categories: java
--- 

有一需求，输入是JSON格式的条件，输出是SQL的where格式的条件。譬如输入：
```
{
  "conditions" : [
    {
      "field" : "a",
      "operator" : "like",
      "values" : [ "'%a%'" ]
    },
    {
      "field" : "b",
      "operator" : "notLike",
      "values" : [ "'%b%'" ]
    },
    {
      "field" : "c",
      "operator" : "greaterThanOrEqualTo",
      "values" : [ "2023-01-01" ]
    }
  ],
  "joint" : "and"
}
```
输出：
```
((a like '%a%') and (b not Like '%b%') and (c greaterThanOrEqualTo "2023-01-01"))
```
如果条件是嵌套条件，输出同样需要，譬如输入：
```
{
  "conditions" : [
    {
      "conditions" : [
        {
          "conditions" : [
            {
              "field" : "a",
              "operator" : "like",
              "values" : [ "'%a%'" ]
            },
            {
              "field" : "b",
              "operator" : "notLike",
              "values" : [ "'%b%'" ]
            }
          ],
          "joint" : "and"
        }, 
        {
          "field" : "c",
          "operator" : "notEquals",
          "values" : [ 1000 ]
        } 
      ],
      "joint" : "or"
    },
    {
      "field" : "d",
      "operator" : "lessThan",
      "values" : [ "2023-01-01" ]
    }
  ],
  "joint" : "and"
} 
```
输出：
```
((((a like '%a%') and (b not Like '%b%')) or (c not Equals 1000)) and (d lessThan "2023-01-01"))
```

第一反应是使用栈，程序如下：
{% highlight java %}
import java.io.*;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class JsonToSqlConditions {
    private String inputFile = "d:/temp/j1.json";

    class Condition {
        String field = "";
        String operator = "";
        String values = "";
    }

    public String getInputFile() {
        return inputFile;
    }

    public void setInputFile(String inputFile) {
        this.inputFile = inputFile;
    }

    public String analyze() throws Exception {
        BufferedReader  br = new BufferedReader(new FileReader(inputFile));
        Stack<String> stack = new Stack<>();
        Condition condition = null;
        String line;

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

            if (line.contains("joint")) {
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

    private Condition setCondition(String line, Condition cond) throws Exception {
        String[] kv = line.split(":");
        String key = "", value = "";

        try {
            key = kv[0].replaceAll("\"", "").trim();
            value = kv[1].replaceAll(",", "").trim();
        }catch (Exception e) {
            throw new Exception("Conditions Format error!");
        }

        if (key.equals("field")) {
            cond.field = value.replaceAll("\"", "");
        }

        if (key.equals("operator")) {
            value = value.replaceAll("\"", "");
            if (value.startsWith("not")) {
                cond.operator = "not " + value.substring(3);
            } else {
                cond.operator = value;
            }
        }

        if (key.equals("values")) {
            Pattern pattern = Pattern.compile("\\[([^\\]]*)\\]");   // starts with '[' and ends with ']'
            Matcher matcher = pattern.matcher(value);

            if (matcher.find()) {
                String val = matcher.group(1).trim();

                if (val.contains("'")) {
                    val = val.replaceAll("\"", "");
                }
                cond.values = val;
            } else {
                throw new Exception("Conditions - values format error!");
            }
        }

        return cond;
    }

    public static void main(String[] args) {
        JsonToSqlConditions j2sConverter = new JsonToSqlConditions();

        if (args.length > 0 && args[0].endsWith(".json")) {
            j2sConverter.setInputFile(args[0]);
        }

        try {
            System.out.println(j2sConverter.analyze());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
{% endhighlight %}