using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetZone.Models;
using System.Text.Json;

namespace PetZone.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AiController : ControllerBase
    {
        private readonly PetZoneDbContext _context;
        private readonly ILogger<AiController> _logger;

        public AiController(PetZoneDbContext context, ILogger<AiController> logger)
        {
            _context = context;
            _logger = logger;
        }

        // ============ AI ALERT ENDPOINTS ============

        /// <summary>
        /// Nhận alert từ AI Service
        /// POST: api/ai/alert
        /// </summary>
        [HttpPost("alert")]
        public async Task<IActionResult> ReceiveAlert([FromBody] AiAlertRequest request)
        {
            _logger.LogInformation("========== AI ALERT RECEIVED ==========");
            _logger.LogInformation($"Alert Level: {request.AlertLevel}");
            _logger.LogInformation($"Message: {request.Message}");
            _logger.LogInformation($"Confidence: {request.Confidence:P}");

            try
            {
                // Lưu alert vào database (có thể tạo bảng AiAlerts)
                var alert = new AiDetection
                {
                    HasPet = request.SensorData?.PresenceEnergy > 0,
                    ConfidenceScore = (decimal)request.Confidence,
                    Note = $"[{request.AlertLevel}] {request.Message}",
                    CreatedAt = DateTime.UtcNow
                };

                _context.AiDetections.Add(alert);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Alert saved with ID: {alert.Id}");
                _logger.LogInformation("=======================================");

                return Ok(new { 
                    message = "Alert received", 
                    id = alert.Id,
                    timestamp = DateTime.UtcNow 
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error saving alert: {ex.Message}");
                return StatusCode(500, new { error = "Failed to save alert" });
            }
        }

        /// <summary>
        /// Nhận emergency alert từ AI Service
        /// POST: api/ai/emergency
        /// </summary>
        [HttpPost("emergency")]
        public async Task<IActionResult> ReceiveEmergency([FromBody] AiEmergencyRequest request)
        {
            _logger.LogWarning("========== 🚨 EMERGENCY ALERT 🚨 ==========");
            _logger.LogWarning($"Alert Type: {request.AlertType}");
            _logger.LogWarning($"Alert Level: {request.AlertLevel}");
            _logger.LogWarning($"Message: {request.Message}");
            _logger.LogWarning($"Actions: {string.Join(", ", request.Actions ?? new List<string>())}");
            _logger.LogWarning("==========================================");

            try
            {
                var alert = new AiDetection
                {
                    HasPet = request.SensorData?.PresenceEnergy > 0,
                    ConfidenceScore = (decimal)request.Confidence,
                    Note = $"[EMERGENCY-{request.AlertLevel}] {request.Message} | Actions: {string.Join(", ", request.Actions ?? new List<string>())}",
                    CreatedAt = DateTime.UtcNow
                };

                _context.AiDetections.Add(alert);
                await _context.SaveChangesAsync();

                // TODO: Send push notification, email, SMS, etc.
                
                return Ok(new { 
                    message = "Emergency alert received", 
                    id = alert.Id,
                    timestamp = DateTime.UtcNow 
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error saving emergency alert: {ex.Message}");
                return StatusCode(500, new { error = "Failed to save emergency alert" });
            }
        }

        /// <summary>
        /// Lấy danh sách alerts gần đây
        /// GET: api/ai/alerts
        /// </summary>
        [HttpGet("alerts")]
        public async Task<IActionResult> GetRecentAlerts([FromQuery] int limit = 20)
        {
            try
            {
                var alerts = await _context.AiDetections
                    .OrderByDescending(a => a.CreatedAt)
                    .Take(limit)
                    .ToListAsync();

                return Ok(alerts);
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error fetching alerts: {ex.Message}");
                return StatusCode(500, new { error = "Failed to fetch alerts" });
            }
        }

        /// <summary>
        /// Lấy alert mới nhất
        /// GET: api/ai/alerts/latest
        /// </summary>
        [HttpGet("alerts/latest")]
        public async Task<IActionResult> GetLatestAlert()
        {
            try
            {
                var alert = await _context.AiDetections
                    .OrderByDescending(a => a.CreatedAt)
                    .FirstOrDefaultAsync();

                if (alert == null)
                    return NotFound(new { message = "No alerts found" });

                return Ok(alert);
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error fetching latest alert: {ex.Message}");
                return StatusCode(500, new { error = "Failed to fetch latest alert" });
            }
        }

        // ============ AI STATUS ENDPOINTS ============

        /// <summary>
        /// Nhận status từ AI pet detection (legacy endpoint)
        /// POST: api/ai/status
        /// </summary>
        [HttpPost("status")]
        public async Task<IActionResult> ReceiveAiStatus([FromBody] AiStatusRequest request)
        {
            _logger.LogInformation($"[AI] Pet Detection: {request.HasPet} (Confidence: {request.Confidence:P})");

            try
            {
                var detection = new AiDetection
                {
                    HasPet = request.HasPet,
                    ConfidenceScore = (decimal)request.Confidence,
                    Note = $"{request.DetectionMethod} at {request.Timestamp}",
                    CreatedAt = DateTime.UtcNow
                };

                _context.AiDetections.Add(detection);
                await _context.SaveChangesAsync();

                return Ok(new { message = "AI status received", id = detection.Id });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error saving AI status: {ex.Message}");
                return StatusCode(500, new { error = "Failed to save AI status" });
            }
        }

        /// <summary>
        /// Lấy trạng thái AI hiện tại
        /// GET: api/ai/status
        /// </summary>
        [HttpGet("status")]
        public async Task<IActionResult> GetAiStatus()
        {
            try
            {
                var latestDetection = await _context.AiDetections
                    .OrderByDescending(d => d.CreatedAt)
                    .FirstOrDefaultAsync();

                var latestSensor = await _context.SensorReadings
                    .OrderByDescending(s => s.CreatedAt)
                    .FirstOrDefaultAsync();

                return Ok(new
                {
                    aiDetection = latestDetection,
                    sensorReading = latestSensor,
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error fetching AI status: {ex.Message}");
                return StatusCode(500, new { error = "Failed to fetch AI status" });
            }
        }
    }

    // ============ REQUEST MODELS ============

    public class AiAlertRequest
    {
        public string AlertLevel { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public double Confidence { get; set; }
        public SensorDataDto? SensorData { get; set; }
        public object? Reasoning { get; set; }
        public DateTime Timestamp { get; set; }
    }

    public class AiEmergencyRequest
    {
        public string AlertType { get; set; } = string.Empty;
        public string AlertLevel { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public double Confidence { get; set; }
        public SensorDataDto? SensorData { get; set; }
        public List<string>? Actions { get; set; }
        public object? Reasoning { get; set; }
        public DateTime Timestamp { get; set; }
    }

    public class AiStatusRequest
    {
        public bool HasPet { get; set; }
        public string DetectionMethod { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public double Confidence { get; set; }
    }

    public class SensorDataDto
    {
        public double Temperature { get; set; }
        public double Humidity { get; set; }
        public int PresenceEnergy { get; set; }
        public int MovementEnergy { get; set; }
    }
}
