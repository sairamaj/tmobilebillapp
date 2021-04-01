using Markdig;

namespace SelfService.Shared
{
    public class GeneralMessage
    {
        public string Message { get; set; }

        public string CurrentMessageAsMarkdown
        {
            get
            {
                if (string.IsNullOrWhiteSpace(this.Message))
                {
                    return string.Empty;
                }

                return Markdown.ToHtml(this.Message);
            }
        }
    }
}