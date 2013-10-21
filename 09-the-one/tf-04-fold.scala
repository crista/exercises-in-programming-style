/**
Attempt to speed up execution time: Avg 4.4 seconds
1. Use a compiled regex
2. accumulate tokens using a catamorphism

$ time scala tf04fold ../pride-and-prejudice.txt
(Mr,786)
(Elizabeth,635)
(very,473)
(Darcy,417)
(such,378)
(Mrs,343)
(much,325)
(more,325)
(Bennet,322)
(Bingley,305)
(Jane,295)
(Miss,281)
(one,261)
(know,239)
(herself,227)
(before,225)
(sister,218)
(never,214)
(soon,214)
(though,212)
(think,210)
(time,203)
(now,197)
(Wickham,194)
(well,188)

real  0m4.392s
*/
object tf04fold extends App {
  def l(f:String) = io.Source.fromFile(f).getLines.mkString(",")
  val s = l("../stop_words.txt").split(",") ++ (1 to 26).map(i=>String.valueOf(Character.toChars(96+i)))
  val p = java.util.regex.Pattern.compile("[^a-zA-Z]+")
  val a:List[Array[String]] = Nil
  val w = io.Source.fromFile(args(0)).getLines.foldLeft(a)((b,c)=> p.split(c).filter(x => (x.length > 0) && !s.contains(x.toLowerCase)) :: b).flatten
  w.distinct.map(u=> (u,w.count(_==u))).sortBy(-_._2).take(25).foreach(println)
}
