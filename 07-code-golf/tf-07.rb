#!/usr/bin/env ruby
require 'set'

stops = ((IO.read '../stop_words.txt').split ',').to_set
ARGF.read.downcase.scan(/[a-z]{2,}/).each_with_object(Hash.new 0){|w,c|c[w]+=1 if not stops.member? w}.sort_by{|w,c|-c}[0,25].each{|w,c|puts "#{w} - #{c}"}

