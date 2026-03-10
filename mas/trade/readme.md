[下單] --> [送出接受 → receive_order_status] 
               ↓
          [等待成交 → receive_order_status] 
               ↓
          [部分成交 → receive_order_execution]
               ↓
          [全部成交 → receive_order_execution]
               ↓
          [訂單完成 → receive_order_status]
