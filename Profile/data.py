"""
File chứa dữ liệu mẫu cho Forum Profile
Import file này để sử dụng dữ liệu
"""

# Dữ liệu Users
USERS = [
    {
        "id": 1,
        "username": "nguyen_van_a",
        "email": "nguyenvana@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=1",
        "bio": "Developer | Tech Enthusiast | Coffee Lover ☕"
    },
    {
        "id": 2,
        "username": "tran_thi_b",
        "email": "tranthib@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=2",
        "bio": "Digital Marketer | Travel Blogger 🌍"
    },
    {
        "id": 3,
        "username": "le_van_c",
        "email": "levanc@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=3",
        "bio": "Gamer | Streamer | Esports Fan 🎮"
    },
    {
        "id": 4,
        "username": "pham_thi_d",
        "email": "phamthid@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=4",
        "bio": "Photographer | Nature Lover 📷"
    },
    {
        "id": 5,
        "username": "hoang_van_e",
        "email": "hoangvane@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=5",
        "bio": "Music Producer | DJ 🎵"
    },
    {
        "id": 6,
        "username": "vo_thi_f",
        "email": "vothif@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=6",
        "bio": "Fitness Coach | Nutrition Expert 💪"
    },
    {
        "id": 7,
        "username": "dang_van_g",
        "email": "dangvang@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=7",
        "bio": "Entrepreneur | Startup Founder 🚀"
    },
    {
        "id": 8,
        "username": "bui_thi_h",
        "email": "buithih@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=8",
        "bio": "Film Critic | Movie Buff 🎬"
    },
    {
        "id": 9,
        "username": "ngo_van_i",
        "email": "ngovani@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=9",
        "bio": "Artist | Illustrator | Designer 🎨"
    },
    {
        "id": 10,
        "username": "duong_thi_k",
        "email": "duongthik@example.com",
        "avatar_url": "https://i.pravatar.cc/150?img=10",
        "bio": "Writer | Book Lover | Tea Addict 📚"
    }
]

# Dữ liệu Forums
FORUMS = [
    {
        "id": 1,
        "name": "Game Mobile",
        "description": "Thảo luận về các game mobile hot nhất",
        "category": "game",
        "created_by": 1
    },
    {
        "id": 2,
        "name": "PC Gaming",
        "description": "Game trên PC, console và máy tính",
        "category": "game",
        "created_by": 1
    },
    {
        "id": 3,
        "name": "Bóng đá Việt Nam",
        "description": "Tin tức và thảo luận về bóng đá trong nước",
        "category": "the_thao",
        "created_by": 2
    },
    {
        "id": 4,
        "name": "Thể hình - Gym",
        "description": "Chia sẻ kinh nghiệm tập gym và dinh dưỡng",
        "category": "the_thao",
        "created_by": 6
    },
    {
        "id": 5,
        "name": "Khởi nghiệp",
        "description": "Cộng đồng startup và doanh nghiệp",
        "category": "kinh_doanh",
        "created_by": 7
    },
    {
        "id": 6,
        "name": "Đầu tư chứng khoán",
        "description": "Thảo luận về đầu tư và tài chính",
        "category": "kinh_doanh",
        "created_by": 7
    },
    {
        "id": 7,
        "name": "Phim Việt Nam",
        "description": "Review và thảo luận phim Việt",
        "category": "phim",
        "created_by": 8
    },
    {
        "id": 8,
        "name": "Hollywood",
        "description": "Phim ảnh quốc tế",
        "category": "phim",
        "created_by": 8
    },
    {
        "id": 9,
        "name": "Nhiếp ảnh",
        "description": "Chia sẻ ảnh và kỹ thuật chụp",
        "category": "nghe_thuat",
        "created_by": 4
    },
    {
        "id": 10,
        "name": "Âm nhạc",
        "description": "Thảo luận về âm nhạc và nghệ sĩ",
        "category": "nghe_thuat",
        "created_by": 5
    }
]

# Dữ liệu Posts
POSTS = [
    {
        "id": 1,
        "title": "Liên Quân Mobile mùa mới có gì hot?",
        "content": "Mùa giải mới của Liên Quân vừa ra mắt với nhiều tướng mới và meta thay đổi. Các bạn nghĩ sao về bản cập nhật này?",
        "image_url": "https://picsum.photos/800/400?random=1",
        "author_id": 1,
        "forum_id": 1
    },
    {
        "id": 2,
        "title": "Top 5 game mobile đáng chơi nhất 2024",
        "content": "Sau khi thử qua nhiều game, mình xin chia sẻ top 5 game mobile hay nhất năm nay. Bao gồm cả game nhập vai, chiến thuật và thể thao.",
        "image_url": "https://picsum.photos/800/400?random=2",
        "author_id": 3,
        "forum_id": 1
    },
    {
        "id": 3,
        "title": "Cyberpunk 2077 sau 2 năm đã xứng đáng chơi chưa?",
        "content": "Game này từng gây thất vọng lớn khi ra mắt. Nhưng sau nhiều bản cập nhật, hiện tại game đã khác xưa rất nhiều. Các bạn nên thử!",
        "image_url": "https://picsum.photos/800/400?random=3",
        "author_id": 3,
        "forum_id": 2
    },
    {
        "id": 4,
        "title": "Đội tuyển Việt Nam chuẩn bị cho Asian Cup",
        "content": "HLV Troussier đã công bố danh sách sơ bộ. Đội hình có nhiều gương mặt trẻ triển vọng. Cùng thảo luận về cơ hội của đội tuyển nhé!",
        "image_url": "https://picsum.photos/800/400?random=4",
        "author_id": 2,
        "forum_id": 3
    },
    {
        "id": 5,
        "title": "Công Phượng ghi bàn cho đội mới",
        "content": "Sau khi sang Nhật Bản thi đấu, Công Phượng đã có bàn thắng đầu tiên. Đây là tín hiệu rất tích cực cho cầu thủ người Việt ở nước ngoài.",
        "image_url": "https://picsum.photos/800/400?random=5",
        "author_id": 2,
        "forum_id": 3
    },
    {
        "id": 6,
        "title": "Lịch tập gym cho người mới bắt đầu",
        "content": "Mình xin chia sẻ lịch tập 3 buổi/tuần phù hợp cho newbie. Tập trung vào các bài cơ bản để xây dựng nền tảng sức khỏe.",
        "image_url": "https://picsum.photos/800/400?random=6",
        "author_id": 6,
        "forum_id": 4
    },
    {
        "id": 7,
        "title": "Kinh nghiệm tăng cân sạch sau 6 tháng",
        "content": "Từ 60kg lên 70kg trong 6 tháng với chế độ ăn khoa học. Chia sẻ thực đơn và cách tập luyện chi tiết.",
        "image_url": "https://picsum.photos/800/400?random=7",
        "author_id": 6,
        "forum_id": 4
    },
    {
        "id": 8,
        "title": "Làm thế nào để gọi vốn startup thành công?",
        "content": "Sau 3 lần pitch, startup của mình đã gọi được vốn Series A. Xin chia sẻ kinh nghiệm và những lỗi cần tránh khi gọi vốn.",
        "image_url": "https://picsum.photos/800/400?random=8",
        "author_id": 7,
        "forum_id": 5
    },
    {
        "id": 9,
        "title": "Xu hướng AI sẽ thay đổi ngành công nghệ",
        "content": "AI đang tác động mạnh đến mọi lĩnh vực. Các startup nên nắm bắt cơ hội này như thế nào để không bị bỏ lại phía sau?",
        "image_url": "https://picsum.photos/800/400?random=9",
        "author_id": 7,
        "forum_id": 5
    },
    {
        "id": 10,
        "title": "Phân tích cổ phiếu VNIndex tháng 10",
        "content": "Thị trường có dấu hiệu tích cực với thanh khoản tăng. Một số cổ phiếu đáng chú ý trong tháng này là VIC, VHM, HPG.",
        "image_url": "https://picsum.photos/800/400?random=10",
        "author_id": 7,
        "forum_id": 6
    },
    {
        "id": 11,
        "title": "Review phim Mai - Trấn Thành",
        "content": "Phim mới của Trấn Thành vừa ra rạp. Nội dung cảm động, diễn xuất tốt nhưng có vài điểm còn chưa thật sự thuyết phục.",
        "image_url": "https://picsum.photos/800/400?random=11",
        "author_id": 8,
        "forum_id": 7
    },
    {
        "id": 12,
        "title": "Oppenheimer thắng Oscar - Xứng đáng hay không?",
        "content": "Phim của Christopher Nolan vừa càn quét các giải Oscar. Các bạn nghĩ sao về chiến thắng này?",
        "image_url": "https://picsum.photos/800/400?random=12",
        "author_id": 8,
        "forum_id": 8
    },
    {
        "id": 13,
        "title": "Hướng dẫn chụp ảnh portrait cho người mới",
        "content": "Những tips cơ bản để chụp ảnh chân dung đẹp: góc chụp, ánh sáng, và cách tạo dáng cho model.",
        "image_url": "https://picsum.photos/800/400?random=13",
        "author_id": 4,
        "forum_id": 9
    },
    {
        "id": 14,
        "title": "Máy ảnh nào phù hợp cho người mới bắt đầu?",
        "content": "So sánh các dòng máy ảnh entry-level từ Canon, Sony, Nikon. Budget khoảng 15-20 triệu.",
        "image_url": "https://picsum.photos/800/400?random=14",
        "author_id": 4,
        "forum_id": 9
    },
    {
        "id": 15,
        "title": "Sơn Tùng MTP comeback với MV mới",
        "content": "MV mới của Sơn Tùng vừa ra mắt và đạt 10 triệu views trong 24h. Các bạn nghĩ sao về sản phẩm lần này?",
        "image_url": "https://picsum.photos/800/400?random=15",
        "author_id": 5,
        "forum_id": 10
    },
    {
        "id": 16,
        "title": "Top 10 bài hát Vpop hay nhất 2024",
        "content": "Tổng hợp những bài hát được yêu thích nhất năm qua. Có cả ballad, pop và rap Việt.",
        "image_url": "https://picsum.photos/800/400?random=16",
        "author_id": 5,
        "forum_id": 10
    },
    {
        "id": 17,
        "title": "Học guitar cho người mới - Nên bắt đầu từ đâu?",
        "content": "Chia sẻ roadmap học guitar từ cơ bản đến nâng cao. Kèm theo các tài liệu và khóa học miễn phí.",
        "image_url": "https://picsum.photos/800/400?random=17",
        "author_id": 5,
        "forum_id": 10
    },
    {
        "id": 18,
        "title": "Review setup gaming cho budget 20 triệu",
        "content": "Chia sẻ config PC gaming và các thiết bị ngoại vi cho ae có ngân sách vừa phải.",
        "image_url": "https://picsum.photos/800/400?random=18",
        "author_id": 1,
        "forum_id": 2
    },
    {
        "id": 19,
        "title": "Bí quyết marketing online hiệu quả",
        "content": "Từ kinh nghiệm làm marketing cho nhiều brand, mình xin chia sẻ những chiến lược đã từng thành công.",
        "image_url": "https://picsum.photos/800/400?random=19",
        "author_id": 2,
        "forum_id": 5
    },
    {
        "id": 20,
        "title": "Món ăn healthy cho người tập gym",
        "content": "20 công thức món ăn ngon, healthy và dễ làm cho người tập thể hình. Đầy đủ protein và vitamin.",
        "image_url": "https://picsum.photos/800/400?random=20",
        "author_id": 6,
        "forum_id": 4
    }
]

# Dữ liệu Comments
COMMENTS = [
    {"content": "Mình cũng đang chơi Liên Quân, meta mới khá cân bằng đấy!", "author_id": 2, "post_id": 1},
    {"content": "Tướng mới quá mạnh, cần nerf gấp", "author_id": 3, "post_id": 1},
    {"content": "Cảm ơn bạn đã chia sẻ! Mình sẽ thử các game này", "author_id": 4, "post_id": 2},
    {"content": "Cyberpunk giờ chơi rất mượt, đồ họa đỉnh!", "author_id": 1, "post_id": 3},
    {"content": "Hy vọng đội tuyển sẽ làm nên bất ngờ tại Asian Cup", "author_id": 1, "post_id": 4},
    {"content": "Công Phượng xứng đáng với thành công này!", "author_id": 3, "post_id": 5},
    {"content": "Lịch tập rất chi tiết, cảm ơn bạn nhiều!", "author_id": 2, "post_id": 6},
    {"content": "Mình cũng đang áp dụng chế độ tương tự, hiệu quả lắm", "author_id": 4, "post_id": 7},
    {"content": "Kinh nghiệm rất hay, mình sẽ tham khảo khi gọi vốn", "author_id": 5, "post_id": 8},
    {"content": "AI thực sự là cơ hội lớn cho các startup", "author_id": 1, "post_id": 9},
    {"content": "Phân tích rất sâu, cảm ơn bạn!", "author_id": 2, "post_id": 10},
    {"content": "Phim hay nhưng hơi dài, có đoạn kéo", "author_id": 4, "post_id": 11},
    {"content": "Oppenheimer xứng đáng với mọi giải thưởng!", "author_id": 1, "post_id": 12},
    {"content": "Tips rất hữu ích cho người mới như mình", "author_id": 3, "post_id": 13},
    {"content": "Mình recommend Canon 200D II cho newbie", "author_id": 9, "post_id": 14},
    {"content": "MV này quality cao hơn những MV trước", "author_id": 10, "post_id": 15},
    {"content": "List này thiếu mất bài ABC của XYZ rồi!", "author_id": 1, "post_id": 16},
    {"content": "Mình đang học guitar theo lộ trình này, rất ổn!", "author_id": 2, "post_id": 17},
    {"content": "Setup này ngon quá, mình sẽ tham khảo!", "author_id": 3, "post_id": 18},
    {"content": "Chiến lược marketing này mình đã áp dụng và thấy hiệu quả", "author_id": 7, "post_id": 19}
]

# Dữ liệu Likes
LIKES = [
    {"user_id": 1, "post_id": 2},
    {"user_id": 1, "post_id": 3},
    {"user_id": 1, "post_id": 5},
    {"user_id": 2, "post_id": 1},
    {"user_id": 2, "post_id": 4},
    {"user_id": 2, "post_id": 6},
    {"user_id": 3, "post_id": 1},
    {"user_id": 3, "post_id": 7},
    {"user_id": 3, "post_id": 8},
    {"user_id": 4, "post_id": 9},
    {"user_id": 4, "post_id": 10},
    {"user_id": 4, "post_id": 12},
    {"user_id": 5, "post_id": 11},
    {"user_id": 5, "post_id": 13},
    {"user_id": 5, "post_id": 14},
    {"user_id": 6, "post_id": 15},
    {"user_id": 7, "post_id": 16},
    {"user_id": 8, "post_id": 17},
    {"user_id": 9, "post_id": 18},
    {"user_id": 10, "post_id": 19}
]

# Dữ liệu Followers
FOLLOWERS = [
    {"follower_id": 1, "following_id": 2},
    {"follower_id": 1, "following_id": 3},
    {"follower_id": 1, "following_id": 4},
    {"follower_id": 1, "following_id": 5},
    {"follower_id": 1, "following_id": 6},
    {"follower_id": 1, "following_id": 7},
    {"follower_id": 1, "following_id": 8},
    {"follower_id": 1, "following_id": 9},
    {"follower_id": 1, "following_id": 10},
    {"follower_id": 2, "following_id": 1},
    {"follower_id": 3, "following_id": 1},
    {"follower_id": 4, "following_id": 1},
    {"follower_id": 5, "following_id": 1},
    {"follower_id": 6, "following_id": 1},
    {"follower_id": 7, "following_id": 1},
    {"follower_id": 8, "following_id": 1},
    {"follower_id": 9, "following_id": 1},
    {"follower_id": 10, "following_id": 1},
    {"follower_id": 2, "following_id": 3},
    {"follower_id": 2, "following_id": 4},
    {"follower_id": 3, "following_id": 2},
    {"follower_id": 3, "following_id": 5},
    {"follower_id": 4, "following_id": 9},
    {"follower_id": 5, "following_id": 10},
    {"follower_id": 6, "following_id": 7},
    {"follower_id": 7, "following_id": 6},
    {"follower_id": 8, "following_id": 9},
    {"follower_id": 9, "following_id": 4},
    {"follower_id": 10, "following_id": 5}
]

# Dữ liệu Status Updates
STATUS_UPDATES = [
    {"content": "Đang làm việc trên dự án mới! 🚀", "user_id": 1},
    {"content": "Vừa hoàn thành khóa học FastAPI, rất hữu ích!", "user_id": 1},
    {"content": "Hôm nay tập gym cực kỳ năng suất 💪", "user_id": 6},
    {"content": "Đang trong chuyến du lịch Đà Lạt, thời tiết tuyệt vời!", "user_id": 2},
    {"content": "Stream game tối nay lúc 8pm, ae vào xem nhé!", "user_id": 3},
    {"content": "Ra ngoài chụp ảnh cả ngày, mệt nhưng vui 📷", "user_id": 4},
    {"content": "Đang sáng tác beat mới cho album sắp tới 🎵", "user_id": 5},
    {"content": "Startup của mình vừa đạt milestone 1000 users! 🎉", "user_id": 7},
    {"content": "Xem phim Marvel mới, khá ổn so với mong đợi", "user_id": 8},
    {"content": "Triển lãm tranh cuối tuần này, mọi người ủng hộ nhé!", "user_id": 9}
]

# Dữ liệu Votes
VOTES = [
    {"user_id": 1, "post_id": 1, "vote_type": "upvote"},
    {"user_id": 1, "post_id": 2, "vote_type": "upvote"},
    {"user_id": 1, "post_id": 8, "vote_type": "upvote"},
    {"user_id": 2, "post_id": 1, "vote_type": "upvote"},
    {"user_id": 2, "post_id": 3, "vote_type": "upvote"},
    {"user_id": 2, "post_id": 4, "vote_type": "upvote"},
    {"user_id": 3, "post_id": 1, "vote_type": "upvote"},
    {"user_id": 3, "post_id": 2, "vote_type": "upvote"},
    {"user_id": 3, "post_id": 3, "vote_type": "upvote"},
    {"user_id": 4, "post_id": 6, "vote_type": "upvote"},
    {"user_id": 4, "post_id": 7, "vote_type": "upvote"},
    {"user_id": 5, "post_id": 8, "vote_type": "upvote"},
    {"user_id": 5, "post_id": 9, "vote_type": "upvote"},
    {"user_id": 6, "post_id": 6, "vote_type": "upvote"},
    {"user_id": 6, "post_id": 7, "vote_type": "upvote"},
    {"user_id": 6, "post_id": 20, "vote_type": "upvote"},
    {"user_id": 7, "post_id": 8, "vote_type": "upvote"},
    {"user_id": 7, "post_id": 9, "vote_type": "upvote"},
    {"user_id": 7, "post_id": 10, "vote_type": "upvote"},
    {"user_id": 8, "post_id": 11, "vote_type": "upvote"},
    {"user_id": 8, "post_id": 12, "vote_type": "upvote"},
    {"user_id": 9, "post_id": 13, "vote_type": "upvote"},
    {"user_id": 9, "post_id": 14, "vote_type": "upvote"},
    {"user_id": 10, "post_id": 15, "vote_type": "upvote"},
    {"user_id": 10, "post_id": 16, "vote_type": "upvote"},
    {"user_id": 10, "post_id": 17, "vote_type": "upvote"},
    {"user_id": 1, "post_id": 5, "vote_type": "downvote"},
    {"user_id": 2, "post_id": 12, "vote_type": "downvote"}
]