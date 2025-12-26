using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetZone.Models;

namespace PetZone.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DeviceController : ControllerBase
    {
        private readonly PetZoneDbContext _context;
        private readonly ILogger<DeviceController> _logger;

        public DeviceController(PetZoneDbContext context, ILogger<DeviceController> logger)
        {
            _context = context;
            _logger = logger;
        }

        // ============ DEVICE ACTIVITY ENDPOINTS ============

        /// <summary>
        /// Ghi log hoạt động thiết bị từ AI IoT Controller
        /// POST: api/device/activity
        /// </summary>
        [HttpPost("activity")]
        public async Task<IActionResult> LogDeviceActivity([FromBody] DeviceActivityRequest request)
        {
            _logger.LogInformation("========== DEVICE ACTIVITY LOG ==========");
            _logger.LogInformation($"Device: {request.DeviceType}");
            _logger.LogInformation($"Action: {request.Action}");
            _logger.LogInformation($"Reason: {request.Reason}");

            try
            {
                var activity = new DeviceActivity
                {
                    DeviceType = request.DeviceType,
                    Action = request.Action,
                    Intensity = request.Intensity,
                    Duration = request.Duration,
                    Reason = request.Reason,
                    Timestamp = request.Timestamp ?? DateTime.UtcNow
                };

                _context.DeviceActivities.Add(activity);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Device activity logged with ID: {activity.Id}");
                _logger.LogInformation("=========================================");

                return Ok(new
                {
                    message = "Device activity logged",
                    id = activity.Id,
                    timestamp = activity.Timestamp
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error logging device activity: {ex.Message}");
                return StatusCode(500, new { error = "Failed to log device activity" });
            }
        }

        /// <summary>
        /// Lấy lịch sử hoạt động thiết bị
        /// GET: api/device/activity
        /// </summary>
        [HttpGet("activity")]
        public async Task<IActionResult> GetDeviceActivities(
            [FromQuery] string? deviceType = null,
            [FromQuery] int limit = 50)
        {
            try
            {
                var query = _context.DeviceActivities.AsQueryable();

                if (!string.IsNullOrEmpty(deviceType))
                {
                    query = query.Where(a => a.DeviceType.ToLower() == deviceType.ToLower());
                }

                var activities = await query
                    .OrderByDescending(a => a.Timestamp)
                    .Take(limit)
                    .ToListAsync();

                return Ok(new
                {
                    deviceType = deviceType ?? "all",
                    count = activities.Count,
                    activities = activities
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error fetching device activities: {ex.Message}");
                return StatusCode(500, new { error = "Failed to fetch device activities" });
            }
        }

        /// <summary>
        /// Lấy hoạt động thiết bị mới nhất
        /// GET: api/device/activity/latest
        /// </summary>
        [HttpGet("activity/latest")]
        public async Task<IActionResult> GetLatestActivity([FromQuery] string? deviceType = null)
        {
            try
            {
                var query = _context.DeviceActivities.AsQueryable();

                if (!string.IsNullOrEmpty(deviceType))
                {
                    query = query.Where(a => a.DeviceType.ToLower() == deviceType.ToLower());
                }

                var activity = await query
                    .OrderByDescending(a => a.Timestamp)
                    .FirstOrDefaultAsync();

                if (activity == null)
                    return NotFound(new { message = "No device activity found" });

                return Ok(activity);
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error fetching latest activity: {ex.Message}");
                return StatusCode(500, new { error = "Failed to fetch latest activity" });
            }
        }

        /// <summary>
        /// Lấy thống kê hoạt động thiết bị
        /// GET: api/device/statistics
        /// </summary>
        [HttpGet("statistics")]
        public async Task<IActionResult> GetDeviceStatistics(
            [FromQuery] DateTime? startDate = null,
            [FromQuery] DateTime? endDate = null)
        {
            try
            {
                var query = _context.DeviceActivities.AsQueryable();

                if (startDate.HasValue)
                    query = query.Where(a => a.Timestamp >= startDate.Value);

                if (endDate.HasValue)
                    query = query.Where(a => a.Timestamp <= endDate.Value);

                var activities = await query.ToListAsync();

                var statistics = new
                {
                    totalActivities = activities.Count,
                    dateRange = new
                    {
                        start = startDate ?? activities.Min(a => a.Timestamp),
                        end = endDate ?? activities.Max(a => a.Timestamp)
                    },
                    byDevice = activities
                        .GroupBy(a => a.DeviceType)
                        .Select(g => new
                        {
                            deviceType = g.Key,
                            count = g.Count(),
                            actions = g.GroupBy(a => a.Action)
                                .Select(ag => new
                                {
                                    action = ag.Key,
                                    count = ag.Count()
                                })
                        }),
                    recentActivities = activities
                        .OrderByDescending(a => a.Timestamp)
                        .Take(10)
                        .Select(a => new
                        {
                            a.DeviceType,
                            a.Action,
                            a.Timestamp,
                            a.Reason
                        })
                };

                return Ok(statistics);
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error fetching device statistics: {ex.Message}");
                return StatusCode(500, new { error = "Failed to fetch device statistics" });
            }
        }

        /// <summary>
        /// Xóa lịch sử thiết bị cũ (cleanup)
        /// DELETE: api/device/activity/cleanup
        /// </summary>
        [HttpDelete("activity/cleanup")]
        public async Task<IActionResult> CleanupOldActivities([FromQuery] int daysOld = 30)
        {
            try
            {
                var cutoffDate = DateTime.UtcNow.AddDays(-daysOld);
                
                var oldActivities = await _context.DeviceActivities
                    .Where(a => a.Timestamp < cutoffDate)
                    .ToListAsync();

                if (!oldActivities.Any())
                {
                    return Ok(new { message = "No old activities to clean up", count = 0 });
                }

                _context.DeviceActivities.RemoveRange(oldActivities);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Cleaned up {oldActivities.Count} old device activities");

                return Ok(new
                {
                    message = "Old activities cleaned up",
                    count = oldActivities.Count,
                    cutoffDate = cutoffDate
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error cleaning up activities: {ex.Message}");
                return StatusCode(500, new { error = "Failed to cleanup activities" });
            }
        }
    }

    // ============ REQUEST MODELS ============

    public class DeviceActivityRequest
    {
        public string DeviceType { get; set; } = string.Empty;
        public string Action { get; set; } = string.Empty;
        public int? Intensity { get; set; }
        public int? Duration { get; set; }
        public string Reason { get; set; } = string.Empty;
        public DateTime? Timestamp { get; set; }
    }
}
