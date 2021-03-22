import java.util.*; 
public class MarpleSolver {

  public static int c(char x)
  {
    return (int)x - 65;
  }
  public static int s(int x)
  {
    return x > 0 ? 1 : x < 0 ? -1 : 0;
  }
  public static boolean any(ArrayList<Integer> cont, int i)
  {
    for(Integer every: cont)
      if(Math.abs(every - i) == 1)
        return true;
    return false;
  }

  public static String solve(String[] clues){
    int count = 0;
    ArrayList<Integer>[] ps = new ArrayList[20];
    ArrayList<Integer>[][] t = new ArrayList[4][5];
    for(int i = 0; i < 20; i++) ps[i] = new ArrayList(){

        private static final long serialVersionUID = 1L;

        {
          add(0);
          add(1);
          add(2);
          add(3);
          add(4);
        }
      };

    while(count++ < 7)
    {
      for(String clue: clues)
      {
        int flago = 0;
        for(int i = 0; i < 20; i++){
          if(ps[i].size() != 1){
            flago = 1;
            break;
          }
        }
        if(flago == 0)
          break;
        if(clue.charAt(1)!='^'&&clue.charAt(1)!='<'&&clue.charAt(0)!=clue.charAt(2))
        { 
          if(ps[c(clue.charAt(1))].size() == 1)
          {
            //If middle element has just one possibility, then remove that location from the first and last
            //element possibility, since first and last element cannot occupy that position
            int key = ps[c(clue.charAt(1))].get(0);
            ps[c(clue.charAt(0))].remove(Integer.valueOf(key));
            ps[c(clue.charAt(2))].remove(Integer.valueOf(key));
        
          }else{
            //Otherwise narrow down the possible range of the middle element to exclusively between the minimum and 
            //maximum of span of the first and last element.
              int mi0 = ps[c(clue.charAt(0))].get(0), ma0 = Collections.max(ps[c(clue.charAt(0))]);
              int mi2 = ps[c(clue.charAt(2))].get(0), ma2 = Collections.max(ps[c(clue.charAt(2))]);
              int mi = mi0 > mi2 ? mi2 : mi0, ma = ma0 > ma2 ? ma0 : ma2;
              ps[c(clue.charAt(1))].removeIf(ele -> ele >= ma || mi >= ele);
          }
          //Get the first and last of possible location of the middle element
          //Here I've assumed that elements are in sorted order, so I'm just taking minimum and maximum element from 
          //the list
          int first = ps[c(clue.charAt(1))].get(0), last = ps[c(clue.charAt(1))].get(ps[c(clue.charAt(1))].size()-1);
          HashSet <Integer> rrr = new HashSet<Integer>();

          //Added all the elements between the first and last in the rrr hash
          for(int i = first; i <= last; i++)
            rrr.add(i);

          int[] fL = new int[]{0, 2};

          /*
          This for loop basically checks if all the possible location of first key or last key lies entirely on
          one side of the possible location of middle element, if yes then remove all of the other side elements
          */
          for(int e: fL)
          { 
            int flag = 0, n0 = 0;
            int elseC = 0;
            int mini = Collections.min(ps[c(clue.charAt(e))]), maxi = Collections.max(ps[c(clue.charAt(e))]);
            HashSet <Integer> eee = new HashSet<Integer>();
            for(int i = mini; i <= maxi; i++)
              eee.add(i);
            eee.retainAll(rrr);

            //eee represents which locations are shared by first or last element with the middle element

            //If none of the location is shared then continue to the next element
            if(eee.size() > 1)
              continue;
            for(int element: ps[c(clue.charAt(e))])
            {
            //if element is bounded by boundaries of the middle clue/key
            //then break the loop, why?
              if(first < element && element < last)
                { elseC = 1; break; }
              else if(element != first && element != last)
              { // In the situation like:
                //          F    L  |      F        L
                //      E           |                    E
                int probable = (element - first)/Math.abs(element - first);
                if(flag != 0 && probable != flag)
                { elseC = 1; break; }
                flag = probable;
              }
              else if((element == first || element == last) && ps[c(clue.charAt(e))].size() == 1)
              {
                if(element == first && element < last)
                  flag = -1;
                else if(element == last && element > first)
                  flag = 1;
              }
            }
            if(elseC == 0)
            {
              if(flag != 0)
              {
                final int secret = flag;
                ps[c(clue.charAt(2-e))].removeIf(el -> !(secret < 0 ? first < el : el < last));
              }
            }
          }
          if(ps[c(clue.charAt(1))].size() == 1)
          {
            //If middle element has just one possibility, then remove that location from the first and last
            //element possibility, since first and last element cannot occupy that position
            int key = ps[c(clue.charAt(1))].get(0);
            ps[c(clue.charAt(0))].remove(Integer.valueOf(key));
            ps[c(clue.charAt(2))].remove(Integer.valueOf(key));
        
          }
          if(ps[c(clue.charAt(2))].size() == 1)
          {
            //If middle element has just one possibility, then remove that location from the first and last
            //element possibility, since first and last element cannot occupy that position
            int key = ps[c(clue.charAt(2))].get(0);
            ps[c(clue.charAt(1))].remove(Integer.valueOf(key));
            ps[c(clue.charAt(0))].remove(Integer.valueOf(key));
        
          }
          if(ps[c(clue.charAt(0))].size() == 1)
          {
            //If middle element has just one possibility, then remove that location from the first and last
            //element possibility, since first and last element cannot occupy that position
            int key = ps[c(clue.charAt(0))].get(0);
            ps[c(clue.charAt(1))].remove(Integer.valueOf(key));
            ps[c(clue.charAt(2))].remove(Integer.valueOf(key));
          }

          //Heuristic 1
          if(ps[c(clue.charAt(1))].size() == 2 && ps[c(clue.charAt(1))].get(0) == 1 && ps[c(clue.charAt(1))].get(1) == 3){
            if(ps[c(clue.charAt(0))].size() == 1 && ps[c(clue.charAt(0))].get(0) == 2){
              ps[c(clue.charAt(2))].removeIf( el -> el == 1 || el == 3);
            }

            if(ps[c(clue.charAt(2))].size() == 1 && ps[c(clue.charAt(2))].get(0) == 2){
              ps[c(clue.charAt(0))].removeIf( el -> el == 1 || el == 3);
            }
          }

          //Heuristic 2
          if(ps[c(clue.charAt(1))].size() == 3 && ps[c(clue.charAt(1))].get(0) == 1 && ps[c(clue.charAt(1))].get(1) == 2 && ps[c(clue.charAt(1))].get(2) == 3){
            if(ps[c(clue.charAt(0))].size() == 5 && ps[c(clue.charAt(2))].equals(ps[c(clue.charAt(1))])){
              ps[c(clue.charAt(0))].removeIf(el -> el == 2);
            }
            if(ps[c(clue.charAt(2))].size() == 5 && ps[c(clue.charAt(0))].equals(ps[c(clue.charAt(1))])){
              ps[c(clue.charAt(2))].removeIf(el -> el == 2);
            }
          }

        }
        else if(clue.charAt(1)=='<')
        {
            ps[c(clue.charAt(0))].removeIf(el -> !(el < ps[c(clue.charAt(2))].get(ps[c(clue.charAt(2))].size()-1)));
            ps[c(clue.charAt(2))].removeIf(el -> !(el > ps[c(clue.charAt(0))].get(0)));
        }
        else if(clue.charAt(1)=='^')
        {
          HashSet <Integer> set1 = new HashSet<Integer>(ps[c(clue.charAt(2))]);
          HashSet <Integer> set2 = new HashSet<Integer>(ps[c(clue.charAt(0))]);
          set1.retainAll(set2);
          ps[c(clue.charAt(2))] = new ArrayList<Integer>(set1);
          ps[c(clue.charAt(0))] = new ArrayList<Integer>(set1);
        }
        else{
          if(ps[c(clue.charAt(0))].size() == 1)
            ps[c(clue.charAt(1))].removeIf(el -> Math.abs(ps[c(clue.charAt(0))].get(0) - el) != 1);
            else if(ps[c(clue.charAt(1))].size() == 2){
            int xX = ps[c(clue.charAt(1))].get(0), yY = ps[c(clue.charAt(1))].get(1);
            ps[c(clue.charAt(0))].removeIf(el -> !(Math.abs(xX - el) == 1 || Math.abs(yY - el) == 1));
          }
          else if(ps[c(clue.charAt(1))].size() != 1){
            ps[c(clue.charAt(0))].removeIf(el -> !any(ps[c(clue.charAt(1))], el));
            ps[c(clue.charAt(1))].removeIf(el -> !any(ps[c(clue.charAt(0))], el));
          }
          else
            ps[c(clue.charAt(0))].removeIf(el -> !any(ps[c(clue.charAt(1))], el));
        } 



        //||After clue
        t = new ArrayList[4][5];
        for(int i = 0; i < 4; i++)
          for(int j = 0; j < 5; j++)
            t[i][j] = new ArrayList<Integer>();
    
        for(int i = 0; i < ps.length ;i++)
          for(Integer num: ps[i])
              t[i/5][num].add(i);

        for(int i = 0; i < 4; i++)
        {
          for(int j = 0; j < 5;j++)
          {
            if(t[i][j].size() == 1)
            {
              ps[t[i][j].get(0)] = new ArrayList();
              ps[t[i][j].get(0)].add(j);
            }
          }
        }

        for(int i = 0; i < 4; i++)
        {
          for(int j = 0; j < 5; j++)
            if(ps[i * 5 + j].size() == 1)
            {
              int w = ps[i * 5 + j].get(0);
              for(int k = 0; k < 5; k++)
              {
                if(k != j){
                  ps[i*5 + k].remove(Integer.valueOf(w));
                }
              }
            }
        }   
      }
    }
    t = new ArrayList[4][5];
    for(int i = 0; i < 4; i++)
      for(int j = 0; j < 5; j++)
        t[i][j] = new ArrayList<Integer>();
  
    for(int i = 0; i < ps.length ;i++)
      for(Integer num: ps[i])
        t[i/5][num].add(i);

    String answer = "";
    for(int i = 0; i < 4; i++)
      for(int j = 0; j < 5; j++)
        answer += Character.toString((char)(t[i][j].get(0) + 65));
    return answer;
  }


  public static void main(String[] args){

    String[] clues = {"MTS", "KTE", "JHO", "RLC", "TRD", "LMA", "TJQ", "SLJ", "MFI", "D^H", "B<I", "DMD", "PHP", "ELE"};
    System.out.println(solve(clues));
  }
}
