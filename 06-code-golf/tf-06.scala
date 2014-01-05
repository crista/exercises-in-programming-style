/**
 Faithful conversion of tf-04.py to scala, avg execution time 5.2 seconds
 $ time scala tf04a ../pride-and-prejudice.txt
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

real  0m5.237s

*/
object tf04 extends App {
  def l(f:String) = io.Source.fromFile(f).getLines.mkString(",")
  val s = l("../stop_words.txt").split(",") ++ (1 to 26).map(i=>String.valueOf(Character.toChars(96+i)))

  l(args(0)).split("[^a-zA-Z]+").filter(x => !s.contains(x.toLowerCase))
  .distinct
  .map(u=> (u,l(args(0)).split("[^a-zA-Z]+").filter(x => !s.contains(x.toLowerCase)).count(_==u)))
  .sortBy(-_._2)
  .take(25)
  .foreach(println)
}
