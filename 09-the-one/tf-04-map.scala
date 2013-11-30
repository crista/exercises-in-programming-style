/**
Attempt to speed up execution time: Avg 0.9 seconds
1. Use a compiled regex
2. accumulate tokens using a catamorphism
3. count tokens using a 2nd catamorphism

$ time scala tf04map ../pride-and-prejudice.txt
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
(soon,214)
(never,214)
(though,212)
(think,210)
(time,203)
(now,197)
(Wickham,194)
(well,188)

real  0m0.882s
*/
object tf04map extends App {
  def l(f:String) = io.Source.fromFile(f).getLines
  val s = l("../stop_words.txt").mkString(",").split(",") ++ (1 to 26).map(i=>String.valueOf(Character.toChars(96+i)))
  val p = java.util.regex.Pattern.compile("[^a-zA-Z]+")
  l(args(0)).foldLeft(Map[String,Int]()){
    (b,c) =>
    p
    .split(c)
    .filter(x => (x.length > 0) && !s.contains(x.toLowerCase))
      .foldLeft(b){
        (d,e) =>
        d ++ Map(e -> (d.getOrElse(e,0)+1))
      }
    }.toSeq
    .sortBy(- _._2)
    .take(25)
    .foreach(println)
}
