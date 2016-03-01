CREATE TABLE `spider_jd_item` (
  `skuid` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '当前商品skuid',
  `product_name` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '商品名称',
  `brand_id` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '品牌id',
  `category1` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '1级分类',
  `category2` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '2级分类',
  `category3` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '3级分类',
  `category4` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '4级分类-品牌名称',
  `price` decimal(12,2) DEFAULT NULL COMMENT '商品价格',
  `price_cost` decimal(12,2) DEFAULT NULL COMMENT '原价',
  `comment_count` int(11) DEFAULT NULL COMMENT '评价总数',
  `update_time` datetime DEFAULT NULL COMMENT '更新日期',
  `re_see_skuid1` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid2` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid3` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid4` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid5` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid6` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid7` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid8` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `re_see_skuid9` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`skuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `spider_jd_comment` (
  `sku_datetime` varchar(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT 'skuid_时间小时',
  `skuid` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '商品skuid',
  `crawl_time` datetime DEFAULT NULL COMMENT '爬取时间',
  `comment_count` int(11) DEFAULT NULL COMMENT '总评价数',
  `good_count` int(11) DEFAULT NULL COMMENT '好评数量',
  `general_count` int(11) DEFAULT NULL COMMENT '中评数量',
  `poor_count` int(11) DEFAULT NULL COMMENT '差评数量',
  `good_rate` int(11) DEFAULT NULL COMMENT '好评率',
  `general_rate` int(11) DEFAULT NULL COMMENT '中评率',
  `poor_rate` int(11) DEFAULT NULL COMMENT '差评率',
  `score1_count` int(11) DEFAULT NULL COMMENT '评分为1的数量',
  `score2_count` int(11) DEFAULT NULL COMMENT '评分为2的数量',
  `score3_count` int(11) DEFAULT NULL COMMENT '评分为3的数量',
  `score4_count` int(11) DEFAULT NULL COMMENT '评分为4的数量',
  `score5_count` int(11) DEFAULT NULL COMMENT '评分为5的数量',
  `average_score` int(11) DEFAULT NULL COMMENT '平均分',
  PRIMARY KEY (`sku_datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;