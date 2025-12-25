using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetZone.Models;

namespace PetZone.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FeedingController : ControllerBase
    {
        private readonly PetZoneDbContext _context;

        public FeedingController(PetZoneDbContext context)
        {
            _context = context;
        }

        // POST: api/Feeding/feed
        // Được gọi từ frontend khi nhấn nút "Cho Ăn Ngay"
        [HttpPost("feed")]
        public async Task<IActionResult> CreateFeedCommand()
        {
            var log = new FeedingLog
            {
                AmountGram = 50,
                IsSuccessful = true,
                TriggerSource = "WEB"
            };

            _context.FeedingLogs.Add(log);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                message = "Feed command created",
                id = log.Id,
                log.AmountGram,
                log.TriggerSource,
                log.CreatedAt
            });
        }

        // GET: api/Feeding/latest
        // Được ESP32 gọi định kỳ để xem có lệnh cho ăn mới không
        [HttpGet("latest")]
        public async Task<IActionResult> GetLatestFeed()
        {
            var latest = await _context.FeedingLogs
                .OrderByDescending(f => f.CreatedAt)
                .FirstOrDefaultAsync();

            if (latest == null)
            {
                return NotFound("Chưa có lệnh cho ăn nào");
            }

            return Ok(latest);
        }
    }
}
