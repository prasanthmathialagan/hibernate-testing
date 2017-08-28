
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

DROP TABLE IF EXISTS `Users`;
CREATE TABLE `Users` (
  `id` bigint NOT NULL,
  `reputation` int(11),
  `createdDate` timestamp,
  `displayName` char(40),
  `lastAccessDate` timestamp,
  `location` char(40),
  `aboutMe` varchar(500),
  `profileImageUrl` varchar(500),
  `websiteUrl` varchar(500),
  `age` smallint,
  `views` int(11),
  `accountId` bigint,
  `upvotes` smallint,
  `downvotes` smallint,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Posts`;
CREATE TABLE `Posts` (
  `id` bigint NOT NULL,
  `postTypeId` smallint,
  `parentId` bigint,
  `acceptedAnswerId` bigint,
  `createdDate` timestamp,
  `score` smallint,
  `views` int(11),
  `ownerUserId` bigint,
  `lastEditorUserId` bigint,
  `lastEditorDisplayName` char(40),
  `lastEditDate` timestamp,
  `lastActivityDate` timestamp,
  `communityOwnedDate` timestamp,
  `closedDate` timestamp,
  `title` varchar(150),
  `tags` varchar(150),
  `answerCount` smallint,
  `commentCount` smallint,
  `favoriteCount` smallint,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `PostHistory`;
CREATE TABLE `PostHistory` (
  `id` bigint NOT NULL,
  `postHistoryTypeId` smallint,
  `postId` bigint,
  `revisionGUID` char(40),
  `createdDate` timestamp,
  `userId` bigint,
  `userDisplayName` char(40),
  `comment` varchar(500),
  `text` varchar(500),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;