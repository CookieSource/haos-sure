# Home Assistant users may keep Sure private while using a publicly trusted
# hostname resolved through local DNS. Upstream Sure derives this callback from
# the current request in production, which is incorrect when opened via ingress.
module HaosEnableBankingCallback
  def enable_banking_callback_url
    configured_url = ENV["ENABLE_BANKING_CALLBACK_URL"].presence
    return configured_url if configured_url

    super
  end
end

Rails.application.config.to_prepare do
  unless ApplicationHelper.ancestors.include?(HaosEnableBankingCallback)
    ApplicationHelper.prepend(HaosEnableBankingCallback)
  end
end
