## 迭代器
场景：
-提供一种可以遍历聚合对象的方式。又称为：游标cursor模式
-聚合对象：存储数据
-迭代器：遍历数据

```java
public class Test {
    public static void main(String[] args) {
        List<Object> list = new ArrayList<>();
        MyList myList = new MyList(list);
        myList.addObject(12);
        myList.addObject(13);
        myList.addObject(14);

        System.out.println(list.size());
        for(MyIterator myIterator=myList.createMyIterator();myIterator.hasNext();myIterator.next()){

            System.out.println(myIterator.getCurrentObj());
        }
    }
}


interface MyIterator{
    boolean isFirst();
    boolean isLast();
    //游标指向第一个元素
    void first();
    //游标指向下一个元素
    void next();
    Object getCurrentObj();
    // 是否有下一个元素
    boolean hasNext();
}

class MyList{
    private List<Object> list;

    public MyList(List<Object> list) {
        this.list = list;
    }

    public void addObject(Object obj){
        list.add(obj);
    }
    public void rmObject(Object obj){
        list.remove(obj);
    }

    public List<Object> getList() {
        return list;
    }

    public void setList(List<Object> list) {
        this.list = list;
    }

    public MyIterator1 createMyIterator(){
        return new MyIterator1();
    }

    private class MyIterator1 implements MyIterator{

        private int cursor=0;

        @Override
        public boolean isFirst() {
            return cursor==0?true:false;
        }

        @Override
        public boolean isLast() {
            return cursor==list.size()-1?true:false;
        }

        @Override
        public void first() {
            cursor = 0;
        }

        @Override
        public void next() {
            if(cursor<list.size()){
                cursor+=1;
            }
        }

        @Override
        public Object getCurrentObj() {
            return list.get(cursor);
        }

        @Override
        public boolean hasNext() {
            if(cursor<list.size()){
                return true;
            }
            return false;
        }
    }
}

```

开发中常见的场景：
-JDK内置的迭代器（List/Set）