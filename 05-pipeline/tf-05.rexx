/* WORDFREQ REXX     Exercises in Programming - CMS Pipelines style  */
/*                   Author: Rob van der Heij, 26 Apr 2019           */

/* Use:                                                              */
/* PIPE (end \) < pridenp txt  | w: wordfreq | cons                  */
/*            \ < stop_wor txt | w:                                  */


alpha = 'A-I a-i J-R j-r S-Z s-z a-i a-i j-r j-r s-z s-z'

'callpipe (end \ name WORDFREQ.REXX:6)',
   '\ *: ',
   '| xlate *-* 00-FF blank' alpha ,  /* Keep words in lower case    */
   '| split ',                        /* .. on separate records      */
   '| locate 2',                      /* At least 2 letters long     */
   '| l: not lookup',                 /* Drop all stop words         */
   '| sort count',                    /* Count the remaining words   */
   '| sort 1.10 d ',                  /* Sort on number of hits      */
   '| take 25',                       /* Take top-25                 */
   '| spec 11-* 1 , - , nw 1.10 strip nw ',    /* Make pretty layout */
   '| *:',
   '\ *.input.1: ',                   /* Read stop words             */
   '| split ,',                       /* .. as one word per line     */
   '| l:'                             /* into lookup table           */

return rc * ( rc <> 12 )
