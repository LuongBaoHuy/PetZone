using System;
using System.Collections.Generic;

namespace PetZone.Models;

public partial class DeviceActivity
{
    public int Id { get; set; }

    public string? DeviceName { get; set; }

    public string? ActionType { get; set; }

    public string? TriggerReason { get; set; }

    public DateTime? CreatedAt { get; set; }
}
