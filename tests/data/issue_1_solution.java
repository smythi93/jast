import java.io.*;
import java.util.*;

public class Solution implements Runnable {
	private BufferedReader in;
	private PrintWriter out;
	private StringTokenizer st;
	private Random rnd;
	
	double Vend;
	
	private double calcFirstSegment(double a, double Vmax, double Vend, double l) {
		double Vl = 0, Vr = Vmax;
		
		for(int it = 0; it < 256; it++) {
			double Vm = (Vl + Vr) / 2.0;
			
			double tFirst = Vm / a;
			
			double tSecond = 0;
			if(Vend < Vm) tSecond = (Vm - Vend) / a;
			
			double firstPart = a * tFirst * tFirst / 2.0;
			double secondPart = Vm * tSecond - a * tSecond * tSecond / 2.0;
			
			double res = firstPart + secondPart;
			
			if(res < l) Vl = Vm;
			else Vr = Vm;
		}
		
		this.Vend = Math.min(Vl, Vend);
		
		double res = 0.0;
		
		{
			double Vm = Vl;
			
			double tFirst = Vm / a;
			double tSecond = 0;
			if(Vend < Vm) tSecond = (Vm - Vend) / a;
			
			//out.println(tSecond);
			
			double firstPart = a * tFirst * tFirst / 2.0;
			double secondPart = Vm * tSecond - a * tSecond * tSecond / 2.0;
			
			double remain = l - firstPart - secondPart;
			
			res = tFirst + tSecond + (remain / Vm);
		}
		
		return res;
	}
	
	private double calcSecondPart(double a, double Vmax, double Vstart, double l) {
		double Vl = Vstart, Vr = Vmax;
		
		//out.println(Vstart);
		
		for(int it = 0; it < 256; it++) {
			double Vm = (Vl + Vr) / 2.0;
			double t = (Vm - Vstart) / a;
			
			double s = Vstart * t + a * t * t / 2.0;
			
			if(s < l) Vl = Vm;
			else Vr = Vm;
		}
		
		double res = 0.0;
		
		{
			double Vm = (Vl + Vr) / 2.0;
			double t = (Vm - Vstart) / a;
			
			double s = Vstart * t + a * t * t / 2.0;
			
			double remain = l - s;
			
			res = t + (remain / Vmax);
		}
		
		return res;
	}
	
	public void solve() throws IOException {
		double a = nextDouble(), v = nextDouble(), l = nextDouble(), d = nextDouble(), w = nextDouble();
		
		double res = calcFirstSegment(a, v, w, d);
		res += calcSecondPart(a, v, Vend, l - d);
		
		out.println(res);
	}
		
	public static void main(String[] args) {
		new Solution().run();
	} 
	
	public void run() {
		try {
			//in = new BufferedReader(new FileReader("input.txt"));
			//out = new PrintWriter(new FileWriter("output.txt"));
			
			in = new BufferedReader(new InputStreamReader((System.in)));
			out = new PrintWriter(System.out);
			
			st = null;
			rnd = new Random();
			
			solve();
			
			out.close();
		} catch(IOException e) {
			e.printStackTrace();
		}	
	}
	
	private String nextToken() throws IOException, NullPointerException {
		while(st == null || !st.hasMoreTokens()) {
			st = new StringTokenizer(in.readLine());
		}
		
		return st.nextToken();
	}
	
	private int nextInt() throws IOException {
		return Integer.parseInt(nextToken());
	}
	
	private long nextLong() throws IOException {
		return Long.parseLong(nextToken());
	}
	
	private double nextDouble() throws IOException {
		return Double.parseDouble(nextToken());
	}

}
