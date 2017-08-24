
DROP TABLE IF EXISTS `Badges`;
CREATE TABLE `Badges` (
  `id` bigint NOT NULL,
  `userId` bigint NOT NULL,
  `name` char(40) NOT NULL,
  `date` timestamp,
  `class` smallint,
  `tagBased` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Comments`;
CREATE TABLE `Comments` (
  `id` bigint NOT NULL,
  `postId` bigint NOT NULL,
  `score` smallint,
  `text` varchar(500) NOT NULL,
  `createdDate` timestamp,
  `userId` bigint,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Tags`;
CREATE TABLE `Tags` (
  `id` bigint NOT NULL,
  `name` char(40) NOT NULL,
  `count` int(11) DEFAULT 0,
  `excerptPostId` bigint,
  `wikiPostId` bigint,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Votes`;
CREATE TABLE `Votes` (
  `id` bigint NOT NULL,
  `postId` bigint NOT NULL,
  `voteTypeId` bigint NOT NULL,
  `createdDate` timestamp,
  `userId` bigint,
  `bountyAmount` int(11),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `PostLinks`;
CREATE TABLE `PostLinks` (
  `id` bigint NOT NULL,
  `createdDate` timestamp,
  `postId` bigint NOT NULL,
  `relatedPostId` bigint NOT NULL,
  `linkTypeId` smallint,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;