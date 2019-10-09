import static org.junit.Assert.*;
import org.junit.Test;


public class testfoo {

	@Test
	public void testFoo() {
        Foo f1 = new Foo();
        String testfoo="abc";
        //测试空字符
        assertTrue(f1.foo("",1).equals("input is null"));
        //测试取第一个字符
        assertTrue(f1.foo(testfoo,0).equals("bc"));
        //测试取最后一个字符
        assertTrue(f1.foo(testfoo,2).equals("ab"));
        assertTrue(f1.foo(testfoo,-1).equals("ab"));
	}

	//测试异常
    @Test(expected= IndexOutOfBoundsException.class)
    public void testFooExp() {
        Foo f1 = new Foo();
        String testfoo="abc";
        assertTrue(f1.foo(testfoo,-4).equals("ab"));
    }

}
