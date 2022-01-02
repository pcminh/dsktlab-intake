# Sử dụng Scrapy thu thập bài báo từ baomoi.com

Sử dụng chuyên trang "Tin mới" (`/tin-moi`) làm điểm bắt đầu

## Chuyên trang "Tin mới" (`/tin-moi`)

Các link đến các bài báo được chứa trong container `div.bm_AC`.
Mỗi một bài báo được chứa trong container `div.bm_E`. 
```
div.bm_AC       Articles containers
    [
    div.bm_E    Article 1
    div.bm_E    Article 2
    div.bm_E    Article 3
    div.bm_E    Article 4
    ...
    div.bm_E    Article n
    ]
```

Trong mỗi một container bài báo (`div.bm_E`), luôn có header `h4.bm_L` 
chứa một anchor gồm tiêu đề, đường link đến bài báo đó
```
div.bm_E                                Article x
    [...]
    div.bm_AF                           Article title container
        h4.bm_L                         Article title h4 header
            span
                a                       Anchor containing attributes "href", "title", "target" and "relt"
                    %ARTICLE_TITLE%
```

Ví dụ một container bài báo có 1 ảnh:
```html
<div class="bm_E">
  <div class="bm_Q">
    <span
      ><a
        href="/du-bao-2022-mot-nam-day-bien-dong-trong-quan-he-my-trung/c/41385755.epi"
        class=""
        title="Dự báo 2022 - một năm đầy biến động trong quan hệ Mỹ - Trung"
        target="_blank"
        rel="noopener noreferrer"
        ><figure class="bm_Bi bm_BL">
          <img
            src="https://photo-baomoi.zadn.vn/w300_r3x2/2022_01_02_30_41385755/72585bf9f2bb1be542aa.jpg"
            alt="Dự báo 2022 - một năm đầy biến động trong quan hệ Mỹ - Trung"
            class="bm_BM"
          /></figure></a
    ></span>
  </div>

  <div class="bm_AG">
    <div class="bm_AF">         <-- Article title container -->
      <h4 class="bm_L">         <-- Article title h4 header -->
        <span
          ><a
            href="/du-bao-2022-mot-nam-day-bien-dong-trong-quan-he-my-trung/c/41385755.epi"
            class=""
            title="Dự báo 2022 - một năm đầy biến động trong quan hệ Mỹ - Trung"
            target="_blank"
            rel="noopener noreferrer"
            >Dự báo 2022 - một năm đầy biến động trong quan hệ Mỹ - Trung</a
          ></span
        >
      </h4>
    </div>
    <div class="bm_R">          <-- Publisher -->
      <a href="/bao-giao-thong/p/30.epi" class="bm_AO"
        ><figure class="bm_Bi bm_BL" aria-label="Logo nhà xuất bản">
          <img
            src="https://photo-baomoi.zadn.vn/c6b35edd839e6ac0338f.png"
            alt=""
            class="bm_BM"
          /></figure></a
      ><time datetime="2022-01-02T07:13:00+07:00">9 giờ</time
      ><a href="/tin-lien-quan/t/23754931.epi" class="bm_F"
        ><span>2 liên quan</span></a
      ><a
        href="/du-bao-2022-mot-nam-day-bien-dong-trong-quan-he-my-trung/c/41385755.epi"
        class="bm_Ec"
        title="Dự báo 2022 - một năm đầy biến động trong quan hệ Mỹ - Trung"
        ><i class="bm_W bm_Gy"></i
      ></a>
    </div>
  </div>
</div>

```

Mỗi trang (ví dụ: `tin-moi/trang1.epi`) có 18 link bài báo.

Khi người dùng duyệt trên chuyên trang và đến các mốc bài báo thứ `n*18-1`, các bài báo mới của trang ngay sau đó
sẽ được tải về (mỗi trang 18 link bài báo) và được thêm vào container `div.bm_AC`. Tối đa 6 trang tiếp theo sẽ
được tải về và thêm vào trước khi người dùng phải bấm vào nút "Trang tiếp" để có thể duyệt tiếp