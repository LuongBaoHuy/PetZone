using System;
using System.Collections.Generic;

namespace PetZone.Models;

public partial class FeedingLog
{
    public int Id { get; set; }

    public int? AmountGram { get; set; }

    public bool? IsSuccessful { get; set; }

    public string? TriggerSource { get; set; }

    public DateTime? CreatedAt { get; set; }
}
