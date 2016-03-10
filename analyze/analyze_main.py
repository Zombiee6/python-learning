# -*- coding: utf-8 -*-
import time

from analyze import comment_manager, incr_manager


class AnalyzeMain(object):

    def __init__(self):
        self.comments = comment_manager.CommentManager()
        self.incr = incr_manager.IncrManager()

    def __incr(self, markXh, incrXh, time_offset, incr, n):
        if not markXh and time_offset >= n:
            incrXh = incr * n / time_offset
            return True, incrXh
        return markXh, incrXh


    def analyze_comments(self, skucomments):
        """
        处理某skuid的所有评论, 处理目的:
        1.计算出不同时间段内的增量情况
        2.删除计算范围以外的评价记录,用来缓解数据量
        :param comments: 某skuid的评价
        :return:
        """

        skuid = skucomments[0]
        first_batch_time = None
        first_comment = None

        incr3h = 0l
        incr6h = 0l
        incr12h = 0l
        incr24h = 0l
        incr48h = 0l
        incr72h = 0l

        mark3h = False
        mark6h = False
        mark12h = False
        mark24h = False
        mark48h = False
        mark72h = False
        markOrver72h = False

        for comment in skucomments[1]:

            batch_time = comment[3]#爬取时间
            if batch_time == None:
                continue
            if first_batch_time == None:
                first_batch_time = batch_time
                first_comment = comment

            else:
                # 最新批次与当前批次的 时间差(小时)
                date_offset = (first_batch_time - batch_time)
                time_offset = date_offset.days * 24 + (date_offset.seconds / 3600)
                # 评论增加量
                incr = first_comment[6] - comment[6]

                mark3h,  incr3h  = self.__incr(mark3h,  incr3h,  time_offset, incr, 3)
                mark6h,  incr6h  = self.__incr(mark6h,  incr6h,  time_offset, incr, 6)
                mark12h, incr12h = self.__incr(mark12h, incr12h, time_offset, incr, 12)
                mark24h, incr24h = self.__incr(mark24h, incr24h, time_offset, incr, 24)
                mark48h, incr48h = self.__incr(mark48h, incr48h, time_offset, incr, 48)
                mark72h, incr72h = self.__incr(mark72h, incr72h, time_offset, incr, 72)

                if markOrver72h:
                    sku_datetime = comment[0]
                    #删除该记录
                    self.comments.rm_old_comment(sku_datetime)
                if mark72h:
                    markOrver72h = True

        return skuid, str(incr3h), str(incr6h), str(incr12h), str(incr24h), str(incr48h), str(incr72h)


    def analyze(self):
        num_none = 0
        num_not_none = 0
        num = 0

        try:
            while self.comments.has_next():
                skucomments = self.comments.next_comments()#<type 'tuple'> [0]skuid, [1]comments
                skuid_incrs_str = self.analyze_comments(skucomments)
                self.incr.upsert_incr(skuid_incrs_str)
                num_not_none += 1

        except Exception as e:
            print e
        finally:
            self.incr.close()
            self.comments.commit_close()

        print "None :", num_none
        print "not None :", num_not_none


if __name__ == '__main__':
    print "-------- analyze --------"
    print "[%s] 程序开始" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    start_time = time.time()

    analyzer = AnalyzeMain()
    print "[%s] analyze初始化完成." % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    analyzer.analyze()

    end_time = time.time()
    print "[%s] 程序结束, 耗时:%.1f分钟" \
          % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), (end_time - start_time) / 60)

